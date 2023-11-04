from async_api.app import App

app = App()

@app.get('')
async def index_page(request):
    return "Hello world"