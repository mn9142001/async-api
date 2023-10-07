from request import Request
from typing import Any
from response import Response
from exception import Http404


class Path:
    def __init__(self, path : str, method : str, callable) -> None:
        self.path : str = path
        self.view = callable
        self.method : str = method
        
    async def match_method(self, method):
        return self.method == method
        
    async def _match(self, url):
        return str(self.path) == str(url)
    
    async def match(self, url : str):
        return await self._match(url)
    
    async def __call__(self, request : Request) -> Any:
        response = await self.view(request)
        response = Response(response, request=request)
        return await response.response

    def __str__(self) -> str:
        return f"{self.path} - {self.view}"


class Router:
    
    def __init__(self) -> None:
        self.routes : list[Path] = []

    async def __call__(self, request : Request =None) -> Any:
        self.request = request
        view = await self.match(request.dest)
        response = await view(self.request)
        return response
    
    def post(self, route):
        def decorator(func):
            def wrapper(request):
                return func(request)
            self.include_path(Path(route, "POST", wrapper))
            return wrapper
        return decorator

    def get(self, route):
        def decorator(func):
            def wrapper(request):
                return func(request)
            self.include_path(Path(route, "GET", wrapper))
            return wrapper
        return decorator
        
    def include_urls(self, urls : list[Path]):
        self.routes += urls
    
    async def match(self, dest):
        for path in self.routes:
            if await path.match(dest) and await path.match_method(self.request.method):
                return path
        raise Http404
        

    
    def include_path(self, path : Path):
        self.routes.append(path)