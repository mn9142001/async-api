from wsgi.request import Request
from wsgi.response import Response

class BaseMiddleWare:
    
    def __init__(self, request=None) -> None:
        self.request = request
        
    def process_request(self, request : Request) -> Request:
        raise NotImplementedError("process request must be implemented")
    
    def process_response(self, response : Response) -> Response:
        raise NotImplementedError("process response must be implemented")