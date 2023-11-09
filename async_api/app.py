from async_api.exception import ApiException
from typing import Any
from async_api.request import Request
from async_api.router import Router, Path
from async_api.router.mixins import ViewIncludeMixin
from async_api.middleware import BaseMiddleWare
from async_api.response import Response
from async_api.config import Config


class App(ViewIncludeMixin):
    request_class = Request

    def __init__(self, middlewares : list[BaseMiddleWare] = [], urls = [], config=Config()) -> None:
        self.load_middlewares(middlewares)
        self.config = config
        self.router = Router()
        self.include_urls(urls)
        
    def load_middlewares(self, middlewares):
        self.middlewares : list[BaseMiddleWare] = [middleware() for middleware in middlewares]
    
    def include_urls(self, urls : list[Path]):
        self.router.include_urls(urls)
        
    def include_router(self, router : Router):
        self.router.include_urls(router.routes)
        
    def include_router_list(self, routers : list[Router]):
        [self.router.include_urls(router.routes) for router in routers]

    def include_path(self, *args, **kwargs):
        return self.router.include_path(*args, **kwargs)

    async def middleware_request_process(self, request : Request) -> Request:
        for middleware in self.middlewares:
            request = await middleware.process_request(request)
        return request
    
    async def middleware_response_process(self, response : Response) -> Response:
        for middleware in reversed(self.middlewares):
            response = await middleware.process_response(response)
        return response

    async def construct_request(self, scope, send, receive) -> Request:
            request = self.request_class(scope, send, receive)
            await request.set_body()
            return request

    async def __call__(self, scope: dict, receive, send) -> Any:
        await self.handle(scope, receive, send)
    
    async def handle(self, scope: dict, receive, send) -> Any:
        self.send = send
        self.receive = receive
        scope['app'] = self

        try:                
            self.request = await self.middleware_request_process(
                await self.construct_request(scope, send=self.send, receive=self.receive)
            )
            
            response = await self.middleware_response_process(
                await self.router(self.request)
            )
            await response.send_response()

        except ApiException as e:
            await self.handle_Exception(e)
            
    async def handle_Exception(self, exception : ApiException):
        message = await self.get_exception_message(exception)
        status = getattr(exception, "status_code", 500)
        await Response(message, status=status, send=self.send).send_body()

    async def get_exception_message(self, exception):
        if hasattr(exception, "message"):
            message = exception.message
        else:
            message = str(exception)
        
        if type(message) == dict:
            return dict
        return {"detail" : message}


