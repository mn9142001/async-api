from request import Request
from typing import Any, Optional
from response import Response
from exception import Http404
from reg import compile_path

class Path:
    
    kwargs = {}
    
    def __init__(self, path : str, method : str, callable) -> None:
        self.path : str = path
        self.view = callable
        self.method : str = method
        self.path_regex = compile_path(path)
        
    async def match_method(self, method) -> bool:
        return self.method == method
        
    async def _match(self, url):
        
        return str(self.path) == str(url)
    
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
    
    def put(self, route):
        def decorator(func):
            def wrapper(request):
                return func(request)
            self.include_path(Path(route, "PUT", wrapper))
            return wrapper
        return decorator
    
    def patch(self, route):
        def decorator(func):
            def wrapper(request):
                return func(request)
            self.include_path(Path(route, "PATCH", wrapper))
            return wrapper
        return decorator
    
    def delete(self, route):
        def decorator(func):
            def wrapper(request):
                return func(request)
            self.include_path(Path(route, "DELETE", wrapper))
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