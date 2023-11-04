from async_api.router.path import ALL_METHODS


class ViewIncludeMixin:
    def route(self, route, methods, *args, **kwargs):
        def decorator(func):
            def wrapper(request):
                return func(request)
            
            self.include_path(route, methods, wrapper, *args, **kwargs)
            return wrapper

        return decorator

    def get(self, route, *args, **kwargs):
        return self.route(route, ["GET"], *args, **kwargs)

    def put(self, route, *args, **kwargs):
        return self.route(route, ["PUT"], *args, **kwargs)

    def patch(self, route, *args, **kwargs):
        return self.route(route, ["PATCH"], *args, **kwargs)

    def delete(self, route, *args, **kwargs):
        return self.route(route, ["DELETE"], *args, **kwargs)

    def post(self, route, *args, **kwargs):
        return self.route(route, ["POST"], *args, **kwargs)

    def register(self, route, methods, *args, **kwargs):
        return self.route(route, methods, *args, **kwargs)  
    
    def register_as_view(self, route, view):
        self.include_path(route, ALL_METHODS, view)