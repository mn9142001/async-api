from async_api.request import Request
from typing import Any, Union
from async_api.response import Response
from async_api.router.reg import compile_path
from pydantic import BaseModel, ValidationError
from async_api import exception
from async_api.structs import MultiValueDict

ALL_METHODS = '__all__'


class Path:
    
    kwargs = {}
    
    def __init__(self, path : str, methods : str, callable, validator : BaseModel = None, validate_many : bool = False) -> None:
        self.validator = validator
        self.validate_many = validate_many        
        self.path : str = f"/{path}"
        self.view = callable
        self.methods = methods
        self.path_regex = compile_path(self.path)
        
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
    async def _validate(validator : BaseModel, obj : Union[dict, MultiValueDict]):
        try:
            to_validate = obj if type(obj) is dict else obj.dict()
            validator.model_validate(to_validate)
        except (ValidationError, exception.ValidationError) as e:
            raise exception.ValidationError(e.errors())
        
    @staticmethod
    async def is_iterator(iterable_obj):
        try:
            assert type(iterable_obj) == list
        except AssertionError as _:
            raise exception.ValidationError("Request body is not iterable")
                
    async def validate(self):
        
        if self.is_validate_many:
            
            await self.is_iterator(await self.request.body)
            
            for obj in await self.request.body:
                await self._validate(self.validator, obj)
                
        else:
            await self.is_mapping(await self.request.body)
            await self._validate(self.validator, await self.request.body)
    
    
    async def __call__(self, request : Request) -> Any:
        self.request = request
        
        if self.is_validate:
            await self.validate()
            
        response : Union[dict, Response] = await self.view(request)
        
        if not isinstance(response, Response):                
            response = Response(response, request=request)
            
        await response.send_response()

    def __str__(self) -> str:
        return f"{self.path} - {self.view}"

