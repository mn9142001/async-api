from functools import cached_property
import json
from exception import Http400
from structs import QueryParameter
from mixins import SendResponseMixin

class Headers:
    def __init__(self, headers={}) -> None:
        [setattr(self, key.decode(), value.decode()) for key, value in headers]
        

class Request(SendResponseMixin):
    kwargs : dict
    
    def __init__(self, scope : dict, send = None, rec = None) -> None:
        self.kwargs = {}
        self.scope = scope
        self.set_scope()
        self.headers = Headers(headers=scope.get('headers', []))
        self.send, self.rec = send, rec
        
    def set_scope(self):
        for key, value in self.scope.items():
            setattr(
                self, 
                key, 
                value.decode() if type(value) == bytes else value
            )
    
    @cached_property
    def params(self) -> QueryParameter:
        return QueryParameter(self.query_string)
    
    @property
    def content_length(self):
        return int((self.headers, b'content-length', b'0'))        
    
    @property
    async def body(self):
        if not hasattr(self, '_body'):
            await self.parse_body()
        return self._body
    
    @property
    def dest(self):
        return self.path
        
    async def parse_body(self):
        if self.method == 'GET':  return
        
        request_body = await self.rec()
        data = request_body.get('body', b'')
        try:
            self._body = json.loads(data)
        except json.JSONDecodeError as e:
            error = f"Error parsing JSON: {str(e)}"
            Http400.message = error
            raise Http400
            