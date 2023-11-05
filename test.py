from async_api.app import App
from async_api.views import View
from async_api.router import Router
from async_api.request import Request

from pydantic import BaseModel

class User:
    name = "mohamed naser"
    age = 15

class UserSchema(BaseModel):
    name : str
    age : int
    
    class Config:
        from_attributes = True


app = App()

@app.post('', response_model=UserSchema)
def index_page(request : Request):
    return User()


@app.get('', response_model=UserSchema, response_is_list=True)
def index_page(request):
    return [User() for _ in range(10)]


@app.get('token')
def get_token(request):
    return "oi"
    
class TestView(View):

    async def get(self):
        return "hello from test page"



router = Router(prefix="blog/")
router.register_as_view("test", TestView.as_view())

app.include_router(router)

