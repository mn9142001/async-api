from .request import Request
from .status import HTTP_200_OK
import json
import tracemalloc
from .mixins import SendResponseMixin
 
tracemalloc.start()

class Response(SendResponseMixin):
    
    def __init__(self, data : dict, request: Request, status = HTTP_200_OK, content_type = "application/json") -> None:
        self.request = request
        self.status = status
        self.content_type = content_type
        self.data = data
        self.headers = []
        
    async def set_header(self, name:str, value:str):
        self.headers.append((name.encode(), value.encode))

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
        headers = self.headers
        headers.append(
            (b'Content-type', self.content_type.encode())
        )
        return headers
    
    async def send_response(self):
        await self.send_body()
    