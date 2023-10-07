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
    return {"message" : "Hello from post index page!", "query" : request.params.query, "body" : await request.body}

@router.get('/favicon.ico')
async def index_page(request : Request):
    return {"message" : "Hello from index page!"}
