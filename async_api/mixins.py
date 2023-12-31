import json
from async_api.exception import ValidationError
from requests_toolbelt.multipart import decoder
from async_api.utils.file import File
from async_api.structs import MultiValueDict
from typing import Union
from async_api.parser import NestedParser

class IsFileException(Exception):
    pass


class SendResponseMixin:
    async def get_scope(self):
        return {
            'type': 'http.response.start',
            'status': self.status,
            'headers': self.get_headers(),
        }
        
    async def _send(self, *args, **kwargs):
        return await self.request.sender(*args, **kwargs)
        
    async def send(self, *args, **kwargs):
        scope = await self.get_scope()
        await self._send(
            scope
        )
        return await self._send(*args, **kwargs)
    

class RequestBodyDecoder:

    def __init__(self) -> None:
        self._data = {}
        self._files = MultiValueDict()
    
    @property
    def files(self) -> Union[dict[str, File], MultiValueDict[str, File]]:
        return self._files

    def make_file(self, headers, content):
        file = File(headers, content)        
        self._files.appendlist(file.name, file)
    
    def formdata_dict_constructor(self, part : decoder.BodyPart):
        headers = part.headers

        if b'Content-Type' in headers and ("filename" in str(headers[b'Content-Disposition'])):
            self.make_file(headers, part.content)
            raise IsFileException

        content_disposition = headers.get(b'Content-Disposition', b'').decode('utf-8')
        name = content_disposition.split('name="')[1].split('"')[0]

        try:        
            content = part.text
        except UnicodeDecodeError as e:
            raise ValidationError(f"{name} is not a text")
        return name, content

    def formdata_decoder(self, data : bytes):
        try:                
            parser = decoder.MultipartDecoder(
                data, self.headers.content_type
            )
        except (decoder.ImproperBodyPartContentException, decoder.NonMultipartContentTypeException) as e:
            raise ValidationError(str(e))

        body = MultiValueDict()

        for part in parser.parts:
            try:                    
                key, value = self.formdata_dict_constructor(part)
            except IsFileException as e:
                continue
            body[key] = value
                    
        self._body = body
        self._body.update(self.files)
        
        nested_parser = NestedParser(self._body)
        
        if nested_parser.is_valid():
            self._body = nested_parser.validate_data
        else:
            raise ValidationError(nested_parser.errors)
        
        self._data.update(self.body.to_data() if hasattr(self.body, 'to_data') else self.body)
        self._data.update(self.files.to_data())

    def json_decoder(self, data):
        try:
            self._body = json.loads(data)
            self._data.update(self._body)
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            error = f"Error parsing JSON: {str(e)}"
            raise ValidationError(error)

    async def get_raw_body(self):
        body = b""
        while True:
            request_body = await self.rec()
            if not 'body' in request_body:
                break
            body += request_body.get('body')

            if not request_body.get('more_body'):
                break
            
        return body

    async def parse_body(self):
        data = await self.get_raw_body()
        
        if self.headers.is_json:
            return self.json_decoder(data)

        elif self.headers.is_multipart:
            return self.formdata_decoder(data)
        
        raise ValidationError("Unknown content-type")

    @property
    def body(self) -> Union[MultiValueDict, dict]:
        if self.method in ['GET', 'DELETE', 'OPTIONS']:  return
        return self._body
    
    @property
    def data(self) -> dict:
        if hasattr(self, '_data'):
            return self._data        
        return self._data
    
    async def set_body(self):
        if not self.method in ['POST', 'PATCH', 'UPDATE']:
            self._body = {}
            return self._body
        
        if not hasattr(self, '_body'):
            await self.parse_body()
        
        return self._body
