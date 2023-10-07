from router import Router
from request import Request
from exception import Http405


class BaseView:
    
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


class HomeView(BaseView):
    
    async def get(self):        
        return "hello from cbv"
    
    
cbv_router = Router()

cbv_router.register_view('/cbv', HomeView.as_view())
