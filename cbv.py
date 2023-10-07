from request import Request
from exception import Http405


class View:
    
    request : Request
    
    @classmethod
    def as_view(cls):
        _cls = cls()
        return _cls.dispatch
    
    async def dispatch(self, request : Request):
        self.request = request
        return await self.call_method()
    
    async def call_method(self):
        method_name = self.request.method.lower()
        view = getattr(self, method_name, None)
        
        if view is None:
            raise Http405
        
        response = await view()
        return response


