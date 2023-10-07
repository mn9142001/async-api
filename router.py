from request import Request
from typing import Any, Optional
from response import Response
from exception import Http404
from reg import compile_path

class Path:
    
    kwargs = {}
    
    def __init__(self, path : str, methods : str, callable) -> None:
        self.path : str = path
        self.view = callable
        self.methods = methods
        self.path_regex = compile_path(path)
        
    async def match_method(self, method) -> bool:
        return method in self.methods
        
    async def match(self, url : str) -> bool:
        match = self.path_regex.match(url)
        if not match: return False

        self.kwargs = match.groupdict()
        return True

    
    async def __call__(self, request : Request) -> Any:
        response : Optional[dict | Response] = await self.view(request)
        if not isinstance(response, Response):                
            response = Response(response, request=request)
        await response.send_response()

    def __str__(self) -> str:
        return f"{self.path} - {self.view}"


class Router:
    
    def __init__(self) -> None:
        self.routes : list[Path] = []

    async def __call__(self, request : Request =None) -> Any:
        self.request = request
        view = await self.match(request.dest)
        self.request.kwargs = view.kwargs
        response = await view(self.request)
        return response
    
    def route(self, route, methods):
            def decorator(func):
                def wrapper(request):
                    return func(request)
                
                path = Path(route, methods, wrapper)
                self.include_path(path)
                return wrapper

            return decorator

    def get(self, route):
        return self.route(route, ["GET"])

    def put(self, route):
        return self.route(route, ["PUT"])

    def patch(self, route):
        return self.route(route, ["PATCH"])

    def delete(self, route):
        return self.route(route, ["DELETE"])

    def post(self, route):
        return self.route(route, ["POST"])
            
    def register(self, route, methods):
        return self.route(route, methods)
            
    def include_urls(self, urls : list[Path]):
        self.routes += urls
    
    async def match(self, dest):
        for path in self.routes:
            if await path.match(dest) and await path.match_method(self.request.method):
                return path
        raise Http404
        

    
    def include_path(self, path : Path):
        self.routes.append(path)