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
    image : FileField


class UserSchema(BaseSchema):
    name : str
    age : int
    multiple_types_allowed_field : [int, str] 
    some_int_list : list[int] #some_int_list[0]
    nested_int_list : list[list[int]] #nested_int_list[0][0]
    profiles : list[UserProfileSchema] #profiles[0].first_name, profiles[0].image
    
    def validate_foo(self, data):
        "capture the value after the built-in validation"
        return data
    
    def validate(self, data):
        "full data validation"
        return super().validate(data)
    
    def pre_validate_foo(self, data):
        "capture the initial raw value without any changes"
        return data

    def serialize_foo(self, data):
        "serialize the field yourself"
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

