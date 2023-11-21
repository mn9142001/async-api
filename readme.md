# A python based backend application that I wrote for fun

### How to use
first thing you need it to initialize an app

```
from async_api.app import App

app = App()
```


if the app is small and consist of small APIs, you can do as following
```
@app.get('')
async def index_page(request):
    return "Hello world"
```

you can also split the application by importing the app object or use your own router

```
from async_api.router import Router
router = Router()

@router.get('admin/{x}/{y}/')
async def admin_page(request : Request):
    
    return {"message" : "Hello from admin page!", "kwarg_x" : request.kwargs['x'], "kwarg_y" : request.kwargs['y']}
```

### that was a basic get view example

#### for post requests
```
@router.post('', validator = UserSchema)
async def index_page(request : Request):
    """You can either return a full response object or the data directly"""
    return {"message" : "Hello from post index page!", "query" : request.params.query, "body" : request.body}
```

You can also access files like that

```
files = request.files
print(files)
```

##### Data can be validated automatically by setting the validator in the post kwargs

###### You can also return the full response yourself

```
from async_api.response import Response

return Response(
    data,
    request
)
```

## Class Based Views can also be used
```
from async_api.views import View

class HomeView(View):
    
    async def get(self):        
        return "hello from cbv"    

router.register_as_view('cbv', HomeView.as_view())
```

we now have the support of nested multipart data thanks to this repo https://github.com/remigermain/nested-multipart-parser/tree/main
```
class UserProfileSchema(BaseSchema):
    first_name : str
    image : FileField


class UserSchema(BaseSchema):
    name : str
    age : int
    some_int_list : list[list[int]]
    profiles : list[UserProfileSchema]
    multiple_types_allowed_field : [int, str]
    nested_int_list : list[list[int]]

you can try such schema with formData easily

{   name : "your name",
    age : 100,
    some_int_list[0] : 1,
    some_int_list[1] : 1,
    some_int_list[2] : 1,
    multiple_types_allowed_field : "hello",
    nested_int_list[0][0] : 1,
    nested_int_list[1][0] : 1,
    profiles[0].first_name : "mohamed",
    profiles[0].image : your file goes here,

}

result will be something like that:

{
    "name": "your name",
    "age": 11,
    "multiple_types_allowed_field": "hello peter",
    "some_int_list": [
        1
    ],
    "nested_int_list": [
        [
            1
        ],
        [
            1
        ]
    ],

    "profiles": [
        {
            "first_name": "mohamed naser",
            "image": "media/file/path/kabtTPE-test.PNG"
        }
    ]
}

```


to get started just do the following

```

pip install git+https://github.com/mn9142001/async-api.git

#install you async interface for example let's use uvicorn
pip install uvicorn

uvicorn app:app 
```

then simply visit http://localhost:8000


