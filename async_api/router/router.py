from .path import Path
from async_api.request import Request
from typing import Any, Union
from async_api.exception import Http404, Http405
from async_api.router.mixins import ViewIncludeMixin

class PathMatchPattern:
    NONE = 0
    PARTIAL = 1
    FULL = 2


class Router(ViewIncludeMixin):

    def __init__(self) -> None:
        self.routes : list[Path] = []

    async def __call__(self, request : Request =None) -> Any:
        self.request = request
        view = await self.match(request.dest)
        self.request.kwargs = view.kwargs
        response = await view(self.request)
        return response

    def include_urls(self, urls : list[Path]):
        self.routes += urls

    async def match(self, dest):
        match_pattern = PathMatchPattern.NONE

        for path in self.routes:
            if await path.match(dest):
                match_pattern = PathMatchPattern.PARTIAL
                if await path.match_method(self.request.method):
                    return path       

        if match_pattern == PathMatchPattern.PARTIAL:
          raise Http405

        raise Http404

    def _include_path(self, path : Path):
        self.routes.append(path)

    def include_path(self, route : str, method : Union[str, list[Path]], view : Any, *args, **kwargs):
        path = Path(route, method, view, *args, **kwargs)
        self._include_path(path)