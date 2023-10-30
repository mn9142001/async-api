from async_api.exception import ApiException
from typing import Any, Union
from async_api.request import Request
from async_api.router import Router, Path
from async_api.middleware import BaseMiddleWare
from async_api.response import Response


class App:
    request_class = Request

    def __init__(self, middlewares : list[BaseMiddleWare] = [], urls = []) -> None:
        self.load_middlewares(middlewares)

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

    async def middleware_request_process(self, request : Request) -> Request:
        for middleware in self.middlewares:
            request = await middleware.process_request(request)
        return request
    
    async def middleware_response_process(self, response : Response) -> Response:
        for middleware in reversed(self.middlewares):
            response = await middleware.process_response(response)
        return response

    async def __call__(self, scope: dict, receive, send) -> Any:
        scope['app'] = self

        try:                
            self.request = await self.middleware_request_process(
                self.request_class(scope, send=send, rec=receive)
            )
            
            response = await self.middleware_response_process(
                await self.router(self.request)
            )
            await response.send_response()

        except ApiException as e:
            await self.handle_Exception(e)
            
    async def handle_Exception(self, exception : ApiException):
        message = await self.get_exception_message(exception.message)
        status = exception.status_code
        await Response(message, request=self.request, status=status).send_body()

    async def get_exception_message(self, message : Union[str, dict]):
        if type(message) == dict:
            return dict
        return {"detail" : message}


