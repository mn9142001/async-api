from async_api.app import App
from async_api.views import View

app = App()

@app.get('')
async def index_page(request):
    return "Hello world"


class TestView(View):
    
    async def get(self):
        return "hello from test page"
    
    
app.register_as_view("test", TestView.as_view())