from response import Response
from router import Router
from request import Request

router = Router()

@router.get('/admin/')
async def admin_page(request : Request):
    return {"message" : "Hello from admin page!"}

@router.get('/')
async def index_page(request : Request):
    return {"message" : "Hello from index page!"}

@router.post('/')
async def index_page(request : Request):
    data = {"message" : "Hello from post index page!", "query" : request.params.query, "body" : await request.body}
    response = Response(
        data,
        request
    )
    return response

@router.get('/favicon.ico')
async def index_page(request : Request):
    return {"message" : "Hello from index page!"}
