import json
from async_api.exception import ValidationError
from requests_toolbelt.multipart import decoder
from async_api.utils.file import File
from async_api.structs import MultiValueDict
from typing import Union


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
    _files = MultiValueDict()
    
    
    @property
    async def files(self) -> Union[dict[str, File], MultiValueDict[str, File]]:
        assert self.headers.is_multipart, "request must be of mulitpart type"
        return self._files

    async def make_file(self, headers, content):
        file = File(headers, content)        
        self._files[await file.name] = file
    
    async def formdata_dict_constructor(self, part : decoder.BodyPart):
        headers = part.headers
        if b'Content-Type' in headers:
            await self.make_file(headers, part.content)
            raise IsFileException

        content_disposition = headers.get(b'Content-Disposition', b'').decode('utf-8')
        name = content_disposition.split('name="')[1].split('"')[0]
        
        try:        
            content = part.text
        except UnicodeDecodeError as e:
            raise ValidationError(f"{name} is not a text")
        return name, content

    async def formdata_decoder(self, data : bytes):
        try:                
            parser = decoder.MultipartDecoder(
                data, self.headers.content_type
            )
        except (decoder.ImproperBodyPartContentException, decoder.NonMultipartContentTypeException) as e:
            raise ValidationError(str(e))
        
        body = MultiValueDict()

        for part in parser.parts:
            try:                    
                key, value = await self.formdata_dict_constructor(part)
            except IsFileException as e:
                continue
            body[key] = value
        self._body = body

    async def json_decoder(self, data):
        try:
            self._body = json.loads(data)
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            error = f"Error parsing JSON: {str(e)}"
            raise ValidationError(error)

    async def get_raw_body(self):
        request_body = await self.rec()
        data = request_body.get('body', b'')
        return data

    async def parse_body(self):
        data = await self.get_raw_body()
        
        if self.headers.is_json:
            return await self.json_decoder(data)

        elif self.headers.is_multipart:
            return await self.formdata_decoder(data)
        
        raise ValidationError("Unknown content-type")

    @property
    async def body(self) -> Union[MultiValueDict, dict]:
        if self.method in ['GET', 'DELETE', 'OPTIONS']:  return
        
        if not hasattr(self, '_body'):
            await self.parse_body()
        
        return self._body
    