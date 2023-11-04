# A python based backend application that I wrote for fun

### How to use

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
    return {"message" : "Hello from post index page!", "query" : request.params.query, "body" : await request.body}
```

You can also access files like that

```
files = await request.files
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


to get started just do the following

```

pip install git+https://github.com/mn9142001/async-api.git

#install you async interface for example let's use uvicorn
pip install uvicorn

uvicorn app:app 
```

then simply visit http://localhost:8000


