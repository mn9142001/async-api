from request import Request
from typing import Any
from status import HTTP_200_OK
import json
import tracemalloc
 
tracemalloc.start()

class Response:
    _content_type = None
    
    def __init__(self, data : dict, request: Request = None, status = HTTP_200_OK) -> None:
        self.request = request
        self.status = status
        self.data = self.parse_data(data)
    
    def parse_data(self, data):
        if type(data) == tuple:
            self.status = data[-1]
            data = data[0]
        return data

    
    async def get_scope(self):
        return {
            'type': 'http.response.start',
            'status': self.status,
            'headers': self.get_headers(),
        }
    
    async def __call__(self, *args: Any, **kwds: Any) -> list[bytes]:
        await self.send_body()
        
    async def _send(self, *args, **kwargs):
        return await self.request.send(*args, **kwargs)
        
    async def send(self, *args, **kwargs):
        scope = await self.get_scope()
        await self._send(
            scope
        )
        return await self._send(*args, **kwargs)
    
    async def send_body(self):
        await self.send({
            'type': 'http.response.body',
            'body': await self.dump_data(),
            'headers' : []
        })
        
    async def dump_data(self):
        response = json.dumps(self.data).encode()
        return response
        
    def get_headers(self):
        headers = []
        headers.append(
            (b'Content-type', self.content_type.encode())
        )
        return headers
    
    @property
    def response(self):
        return self()
    
    @property
    def content_type(self):
        return self._content_type or "application/json"