from .path import Path, ALL_METHODS
from async_api.request import Request
from typing import Any, Union
from async_api.exception import Http404, Http405

class PathMatchPattern:
    NONE = 0
    PARTIAL = 1
    FULL = 2

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
    
    def register_as_view(self, route, view):
        self.include_path(route, ALL_METHODS, view)
            
    def include_urls(self, urls : list[Path]):
        self.routes += urls
    
    async def match(self, dest):
        view = None
        match_pattern = PathMatchPattern.NONE

        for path in self.routes:
            if await path.match(dest):
                match_pattern = PathMatchPattern.PARTIAL
                if await path.match_method(self.request.method):
                    match_pattern = PathMatchPattern.FULL
                    view = path
                    break

        if match_pattern == PathMatchPattern.PARTIAL:
          raise Http405

        if match_pattern == PathMatchPattern.FULL:
            return view

        raise Http404

    def _include_path(self, path : Path):
        self.routes.append(path)
    
    def include_path(self, route : str, method : Union[str, list[Path]], view : Any, *args, **kwargs):
        path = Path(route, method, view, *args, **kwargs)
        self._include_path(path)