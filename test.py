from async_api.app import App
from async_api.views import View
from async_api.router import Router
from async_api.request import Request
from async_api.config import Config as AsyncConfig
from async_api.serializers import BaseSchema, FileField


class User:
    name = "mohamed naser"
    age = 15


class UserProfileSchema(BaseSchema):
    first_name : str

class UserSchema(BaseSchema):
    name : str
    age : [int, str]
    image : list[FileField]
    # profile : [list[UserProfileSchema], None]
    
    def validate_foo(self, data):
        return data
    
    def validate(self, data):
        return super().validate(data)
    
    def pre_validate_foo(self, data):
        return data

    def serialize_foo(self, data):
        pass


class Config(AsyncConfig):
    SECRET_KEY = "asokfafok"


app = App(config=Config())

@app.post('', validator=UserSchema)
def index_page(request : Request):
    return request.validated_body


@app.register('multiple-methods', methods=["GET", "POST"], response_model=UserSchema)
def index_page(request : Request):
    return User()


@app.get('', response_model=UserSchema, response_is_list=True)
def index_page(request):
    return [User() for _ in range(10)]


@app.get('token')
def get_token(request):
    return [request, {"id" : 100}]

class TestView(View):

    async def get(self):
        return "hello from test page"



router = Router(prefix="blog/")
router.register_as_view("test", TestView.as_view())

app.include_router(router)

