from wsgi.request import Request
from typing import Any, Optional
from wsgi.response import Response
from .reg import compile_path
from wsgi.schema import BaseModel
from pydantic import ValidationError
from wsgi import exception

ALL_METHODS = '__all__'


class Path:
    
    kwargs = {}
    
    def __init__(self, path : str, methods : str, callable, validator : BaseModel = None, 
                 validate_many : bool = False, response_schema : BaseModel = None
                ) -> None:
        self.validator = validator
        self.response_schema = response_schema
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
    async def validate_mapping(obj):
        if type(obj) == dict:
            return True
        raise exception.ValidationError("Object is not a valid mapping")

    @property
    def is_validate(self):
        return (self.request.method == "POST") and (self.validator is not None)

    @property
    def is_validate_many(self):
        return self.validate_many

    @staticmethod
    async def _validate(validator : BaseModel, obj : dict):
        try:
            validator(**obj)
        except ValidationError as e:
            raise exception.ValidationError(e.errors())
        
    @staticmethod
    async def is_iterator(iterable_obj, raise_exception=True):
        try:
            assert hasattr(iterable_obj, '__iter__')
            return True
        except AssertionError as _:
            if raise_exception:                    
                raise exception.ValidationError("Request body is not iterable")
            return False
                
    async def validate(self):
        
        if self.is_validate_many:
            
            await self.is_iterator(await self.request.body)
            
            for obj in await self.request.body:
                await self._validate(self.validator, obj)
                
        else:
            await self.validate_mapping(await self.request.body)
            await self._validate(self.validator, await self.request.body)
    
    
    async def __call__(self, request : Request) -> Any:
        self.request = request
        
        if self.is_validate:
            await self.validate()
            
        response : Optional[dict | Response] = await self.view(request)
        
        await self.process_response(response)

    async def _generate_scheme_response(self, data):
        if await self.is_iterator(data, raise_exception=False):
            return [self.response_schema.model_validate(obj).model_dump() for obj in data]
        return "s"

    async def generate_scheme_response(self, data):
        data = await self._generate_scheme_response(data)
        response = Response(data, request=self.request)
        await response.send_response()
    
    async def generate_response(self, data):
        if self.response_schema:
            return await self.generate_scheme_response(data)
        response = Response(data, request=self.request)
        await response.send_response()

    async def process_response(self, response):
        if isinstance(response, Response):                
            await response.send_response()
        await self.generate_response(response)    

    def __str__(self) -> str:
        return f"{self.path} - {self.view}"

