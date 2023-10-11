from wsgi.exception import ApiException
from typing import Any, Optional
from wsgi.request import Request
from wsgi.router import Router
from wsgi.middleware import BaseMiddleWare
from wsgi.response import Response


class App:

    def __init__(self, middlewares : list[BaseMiddleWare]=[], urls = []) -> None:
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
        message = await self.get_exception_message(exception.message)
        status = exception.status_code
        await Response(message, request=self.request, status=status).send_body()

    async def get_exception_message(self, message : Optional[str | dict]):
        if type(message) == dict:
            return dict
        return {"detail" : message}


