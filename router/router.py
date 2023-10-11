from .path import Path, ALL_METHODS
from wsgi.request import Request
from typing import Any, Optional
from wsgi.exception import Http404


class Router:
    
    def __init__(self) -> None:
        self.routes : list[Path] = []

    async def __call__(self, request : Request =None) -> Any:
        self.request = request
        view = await self.match(request.dest)
        self.request.kwargs = view.kwargs
        response = await view(self.request)
        return response
    
    def route(self, route, methods, *args, **kwargs):
        def decorator(func):
            def wrapper(request):
                return func(request)
            
            self.include_path(route, methods, wrapper, *args, **kwargs)
            return wrapper

        return decorator

    def get(self, route, *args, **kwargs):
        return self.route(route, ["GET"], *args, **kwargs)

    def put(self, route, *args, **kwargs):
        return self.route(route, ["PUT"], *args, **kwargs)

    def patch(self, route, *args, **kwargs):
        return self.route(route, ["PATCH"], *args, **kwargs)

    def delete(self, route, *args, **kwargs):
        return self.route(route, ["DELETE"], *args, **kwargs)

    def post(self, route, *args, **kwargs):
        return self.route(route, ["POST"], *args, **kwargs)
            
    def register(self, route, methods, *args, **kwargs):
        return self.route(route, methods, *args, **kwargs)
    
    def register_as_view(self, route, view, *args, **kwargs):
        self.include_path(route, ALL_METHODS, view, *args, **kwargs)
            
    def include_urls(self, urls : list[Path]):
        self.routes += urls
    
    async def match(self, dest):
        for path in self.routes:
            if await path.match(dest) and await path.match_method(self.request.method):
                return path
        raise Http404

    def _include_path(self, path : Path):
        self.routes.append(path)
    
    def include_path(self, route : str, method : Optional[str | list[Path]], view : Any, *args, **kwargs):
        path = Path(route, method, view, *args, **kwargs)
        self._include_path(path)