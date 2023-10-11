from wsgi.app import App
from urls import urls

app = App(urls=urls)