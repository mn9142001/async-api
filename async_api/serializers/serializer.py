
class SerializerMixin:

    @property
    def data(self):
        if not hasattr(self, 'instance'):
            raise Exception("you can't call .data without passing an instance")

        if hasattr(self, '_data'):
            return self._data

        self._data = self.to_representation()

        return self._data

    def get_instance_field_data(self, field_name):
        return getattr(self.instance, field_name, None)

    def serialize_nested_field(self, field_name, field):
        serializer = field(
            instance=self.get_instance_field_data(field_name)
        )
        return serializer.data

    def serialize_field_list(self, field_name, field_list : list):
        data = self.get_instance_field_data(field_name)
        
        if data is None:
            if hasattr(self.__class__, field_name):
                return getattr(self.__class__, field_name)
            return None
        
        for field in field_list:
            if field is None: return data

            try:
                return field(data)
            except ValueError as e:
                continue

    def to_representation(self):
        serialized_data = {}
        
        for field_name, field in self.get_fields():
            
            if self.is_iterable(field):
                serialized_data[field_name] = self.serialize_field_list(field_name=field_name, field_list=field)

            elif self.is_nested_field(field):
                serialized_data[field_name] = self.serialize_nested_field(field=field, field_name=field_name)

            else:
                serialized_data[field_name] = self.get_instance_field_data(field_name)

        return serialized_data
    
    @classmethod
    def serialize_model(cls, obj, many=False):

        if many:
            serializer = [cls(instance=o) for o in obj]
            return [s.data for s in serializer]

        serializer = cls(instance=obj)
        return serializer.data
