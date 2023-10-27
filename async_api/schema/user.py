from pydantic import BaseModel, validator
from async_api import exception


class PasswordMixin:
    password : str
    
    @validator("password")
    def password_validator(cls, password : str):
        if len(password) < 6:
            raise exception.ValidationError("password is too short")
        return password


class UserSchema(PasswordMixin, BaseModel):
    username : str

