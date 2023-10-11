from exception import ApiException
from typing import Any
from request import Request
from router import Router
from views import example_router
from middleware import BaseMiddleWare
from response import Response

urls = [
    
] + example_router.routes 

class App:

    def __init__(self, middlewares : list[BaseMiddleWare]=[]) -> None:
        self.router = Router()
        self.middlewares = middlewares
        self.include_urls(urls)
    
    def include_urls(self, urls):
        self.router.include_urls(urls)
        
    def include_router(self, router : Router):
        self.router.include_urls(router.routes)
    
    async def __call__(self, scope: dict, rec, send, **kwargs: Any) -> Any:
        scope['app'] = self
        try:                
            self.request = Request(scope, send=send, rec=rec)
            response = self.router(self.request)
            await response
        except ApiException as e:
            await self.handle_Exception(e)
            
    async def handle_Exception(self, exception : ApiException):
        message = {"detail" : exception.message}
        status = exception.status_code
        await Response(message, request=self.request, status=status).send_body()


app = App()
