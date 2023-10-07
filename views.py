from response import Response
from router import Router
from request import Request

router = Router()

@router.get('/admin/{x}/{y}/')
async def admin_page(request : Request):
    return {"message" : "Hello from admin page!"}

@router.get('/')
async def index_page(request : Request):    
    return "Hello world!"

@router.post('/')
async def index_page(request : Request):
    """You can either return a full response object or the data directly"""
    
    data = {"message" : "Hello from post index page!", "query" : request.params.query, "body" : await request.body}
    response = Response(
        data,
        request
    )
    return response

@router.register('/test', methods=["GET", "POST"])
async def index_page(request : Request):
    print(await request.body)
    if request.method == 'GET':
        return "This is a get request"
    return {"message" : "Hello from post test page!"}

