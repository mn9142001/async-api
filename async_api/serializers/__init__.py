from async_api.serializers import exceptions
from typing import Any
from collections.abc import Iterable   
from async_api.serializers.validator import ValidatorMixin
from async_api.serializers.serializer import SerializerMixin
from types import GenericAlias

class BaseSchema(ValidatorMixin, SerializerMixin):
    errors : dict

    def __init__(self, instance : Any = None, data : dict = None, context={}, root=None) -> None:
        self.context = context
        self.root = root

        if instance is not None:
            self.instance = instance

        elif data is not None:                
            self.initial_data = data
            self.errors = {}

        else:
            raise exceptions.SerializerException("no data nor instance is passed to the serializer")

    @staticmethod
    def is_nested_field(field):
        return issubclass(field, BaseSchema)

    @staticmethod
    def is_iterable(obj):
        return isinstance(obj, Iterable)

    def get_fields(self):
        for annotation_name, annotation_field in self.__annotations__.items():
            yield (annotation_name, annotation_field)

    @staticmethod
    def is_generic_alias(field):
        return type(field) == GenericAlias

