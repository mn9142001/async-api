from async_api.request import Request
from typing import Any, Union
from async_api.response import Response
from async_api.router.reg import compile_path
from async_api.serializers import BaseSchema
from async_api import exception
from async_api.structs import MultiValueDict
import logging
from inspect import iscoroutinefunction


ALL_METHODS = '__all__'


class Path:
    
    kwargs = {}
    
    def __repr__(self) -> str:
        return f"<{self.path} - Path object>"
    
    def __init__(self, path : str, methods : str, callable, validator : BaseSchema = None, validate_many : bool = False, response_model : BaseSchema =None, response_is_list=False) -> None:
        self.response_model : BaseSchema = response_model
        self.response_is_list = response_is_list
        self.validator = validator
        self.validate_many = validate_many        
        if path.startswith("/"):
            logging.warning(f"Included route {path} starts with /, all routes automatically starts with a /")
        self.path : str = f"/{path}"
        self.view = callable
        self.methods = methods
        self.path_regex = compile_path(self.path)
        
    def add_path_prefix(self, prefix : str):
        self.path = prefix + self.path
        
    async def match_method(self, method) -> bool:
        return (self.methods == ALL_METHODS) or (method in self.methods)
        
    async def match(self, url : str) -> bool:
        match = self.path_regex.match(url)
        if not match: return False

        self.kwargs = match.groupdict()
        return True

    @staticmethod
    async def is_mapping(obj):
        if issubclass(obj.__class__, dict):
            return True
        raise exception.ValidationError("Object is not a valid mapping")

    @property
    def is_validate(self):
        return (self.request.method == "POST") and (self.validator is not None)

    @property
    def is_validate_many(self):
        return self.validate_many
        
    @staticmethod
    async def is_iterator(iterable_obj):
        try:
            assert type(iterable_obj) == list
        except AssertionError as _:
            raise exception.ValidationError("Request body is not iterable")
                
    async def validate(self):

        if self.is_validate_many:
            self.request.validated_body = self.validator.validate_list(self.request.body)

        else:
            await self.is_mapping(self.request.data)
            self.request.validated_body = self.validator.validate_dict(self.request.data)

    @property
    def is_coroutine(self) -> bool:
        return iscoroutinefunction(self.view)

    async def call_view(self):
        if self.is_coroutine:
            response = await self.view(self.request)
        else:
            response = self.view(self.request)

        if self.response_model:
            response = self.response_model.serialize_model(response, many=self.response_is_list)
                
        return response

    async def __call__(self, request : Request) -> Any:
        self.request = request
        
        if self.is_validate:
            await self.validate()
            
        response : Union[dict, Response] = await self.call_view()
        
        if not isinstance(response, Response):                
            response = Response(response, request=request)
        
        return response    

    def __str__(self) -> str:
        return f"{self.path} - {self.view}"

