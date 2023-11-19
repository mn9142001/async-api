from .base import BaseSchema
from async_api.utils.file import File
from . import exceptions

class FileField(BaseSchema):
    initial_data : File
    
    def full_validate(self):
        if not isinstance(self.initial_data, File):
            raise exceptions.ValidationError(message="not_a_file")
        
        self._validated_data = self.initial_data.path
        self._is_valid = True
        
        return self._validated_data
