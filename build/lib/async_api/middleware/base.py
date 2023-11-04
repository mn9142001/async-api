from async_api.request import Request
from async_api.response import Response

class BaseMiddleWare:
    
    async def process_request(self, request : Request) -> Request:
        return request

    async def process_response(self, response : Response) -> Response:
        return response