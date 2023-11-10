from async_api.exception import ValidationError


class SerializerException(Exception):
    status_code = 500


class SkipField(Exception):
    pass

