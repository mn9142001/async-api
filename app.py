from async_api.app import App
from urls import urls


app = App()

app.include_urls(urls)