from async_api.serializers import exceptions
from types import GenericAlias

class ValidatorMixin:
    
    def is_valid(self, raise_exceptions=False):
        if hasattr(self, '_is_valid'):
            return self._is_valid
        
        self.full_validate()
        
        if self.errors:
            self._is_valid = False
        
        else:
            self._is_valid = True
            
        if raise_exceptions and self.errors:
            raise exceptions.ValidationError(message=self.errors)
        
        return self._is_valid
    
    def _validate_field_data(self, field, data):
        if data is None:
            raise exceptions.ValidationError("missing")
        try:
            _validated_data = field(data)
            return _validated_data
        except ValueError as e:
            raise exceptions.ValidationError(message=str(e))

    def validate_multiple_types(self, field_list : list, data):
        error = ""
    
        if data is None and None in field_list:
            raise exceptions.SkipField
    
        for field in field_list:
    
            if self.is_nested_field(field):
                _field : ValidatorMixin = field(data=data, root=self)
                _field.is_valid(raise_exceptions=True)
                return _field._validated_data
            
            if self.is_generic_alias(field):
                return self.validate_generic_alias_field(field=field, data=data)
    
            try:                    
                _validated_data = self._validate_field_data(
                    field=field, data=data
                )
                return _validated_data

            except exceptions.ValidationError as e:
                error = e
                continue
        raise exceptions.ValidationError(error)

        
        
    def validate_selective_field(self, field_name : str, field_list : list, data):
        if data is None and hasattr(self, field_name):
            return getattr(self, field_name)

        if (None in field_list) and data is None:    
            raise exceptions.SkipField

        return self.validate_multiple_types(field_list=field_list, data=data)

    def get_data_for_field(self, field_name):
        return self.initial_data.get(field_name)
    
    def validate_generic_alias_field(self, field : GenericAlias, data):
        origin_class = field.__origin__
        field_list = field.__args__
        validated_data = []
        assert origin_class == list, "list is the only generic alias supported for now."
        
        if data is None:
            if None in field_list:
                raise exceptions.SkipField
            raise exceptions.ValidationError("missing")
                
        for d in data:
            validated_d = self.validate_multiple_types(field_list=field_list, data=d)
            validated_data.append(validated_d)
        return validated_data

    def validate_field(self, field, data):

        if self.is_nested_field(field):
            _field : ValidatorMixin = field(data=data, root=self)
            _field.is_valid(raise_exceptions=True)
            return _field._validated_data

        else:
            return self._validate_field_data(
                field, data=data
            )

    def _validate_field(self, field_name, field):
        field_data = self.get_data_for_field(field_name)

        if hasattr(self, f"pre_validate_{field_name}"):
            validator = getattr(self, f"pre_validate_{field_name}")
            return validator(data=field_data)

        if self.is_generic_alias(field):
            return self.validate_generic_alias_field(field=field, data=field_data)
        
        elif self.is_iterable(field):
            return self.validate_selective_field(field_name=field_name, field_list=field, data=field_data)        

        return self.validate_field(
            field=field,
            data=self.get_data_for_field(field_name)
        )

    def full_validate(self):
        _validated_data = {}
        for field_name, field in self.get_fields():
            try:
                validated_field_data = self._validate_field(field_name=field_name, field=field)
                
                if hasattr(self, f"validate_{field_name}"):
                    validator = getattr(self, f"validate_{field_name}")
                    validated_field_data = validator(data=validated_field_data)

                _validated_data[field_name] = validated_field_data

            except exceptions.SkipField as e:
                continue

            except exceptions.ValidationError as e:
                self.errors[field_name] = e.message
        
        if not self.errors:
            self._validated_data = self.validate(_validated_data)
        
    def validate(self, data):
        return data

    @property
    def validated_data(self):
        if not hasattr(self, '_is_valid'):
            raise Exception("You can't call validated_data before calling is_valid()")
        
        elif self.errors:
            raise Exception("data is not valid, no validated data is here.")
        
        else:
            return self._validated_data
    
    @classmethod
    def validate_list(cls, data : list[dict]):
        serializers = [cls(data=d) for d in data]
        validated_data = []
        
        for serializer in serializers:
            serializer.is_valid(raise_exceptions=True)
            validated_data.append(serializer.validated_data)
            
        return validated_data
    
    @classmethod
    def validate_dict(cls, data : dict):
        serializer = cls(data=data)
        serializer.is_valid(raise_exceptions=True)
        return serializer.validated_data