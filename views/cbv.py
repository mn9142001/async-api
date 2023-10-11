from wsgi.request import Request
from wsgi.exception import Http405


class View:
    
    request : Request
    
    def __init__(self, request : Request) -> None:
        self.request = request
    
    @classmethod
    def as_view(cls):
        return cls.dispatch
    
    @classmethod
    async def dispatch(cls, request : Request):
        view = cls(request)
        return await view.call_method()
    
    async def call_method(self):
        method_name = self.request.method.lower()
        view = getattr(self, method_name, None)
        
        if view is None:
            raise Http405
        
        response = await view()
        return response


