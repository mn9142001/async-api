from wsgi import status

class ApiException(Exception):
    message : str
    status_code : int
    
    def __init__(self, message=None, *args) -> None:
        if message:
            self.message = message
        super().__init__(*args)


class Http404(ApiException):
    message = "Destination not found."
    status_code = status.HTTP_404_NOT_FOUND


class Http405(ApiException):
    message = "method not allowed."
    status_code = status.HTTP_405_METHOD_NOT_ALLOWED
    
    
class ValidationError(ApiException):
    message = "bad request"
    status_code = status.HTTP_400_BAD_REQUEST
    
    