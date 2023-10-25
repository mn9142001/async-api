from wsgi.response import Response
from wsgi.router import Router
from wsgi.request import Request
from wsgi.schema import UserSchema
from wsgi.views import View

router = Router()

@router.get('admin/{x}/{y}/')
async def admin_page(request : Request):
    return {"message" : "Hello from admin page!", "kwarg_x" : request.kwargs['x'], "kwarg_y" : request.kwargs['y']}

@router.get('')
async def index_page(request : Request):    
    return "Hello world!"

@router.post('', validator = UserSchema)
async def index_page(request : Request):
    files = await request.files

    """You can either return a full response object or the data directly"""

    data = {"message" : "Hello from post index page!", "query" : request.params.query, "body" : await request.body}
    response = Response(
        data,
        request
    )
    return response

@router.register('test', methods=["GET", "POST"])
async def index_page(request : Request):
    if request.method == 'GET':
        return "This is a get request"
    return {"message" : "Hello from post test page!"}


class HomeView(View):
    
    async def get(self):        
        return "hello from cbv"    


router.register_as_view('cbv', HomeView.as_view())
