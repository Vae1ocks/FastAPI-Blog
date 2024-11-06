from typing import Annotated
from datetime import datetime
from annotated_types import MinLen, MaxLen

from pydantic import BaseModel, EmailStr, model_validator


class BaseUser(BaseModel):
    username: Annotated[str, MinLen(3), MaxLen(25)]
    email: EmailStr


class PasswordScheme(BaseModel):
    password: Annotated[str, MinLen(8)]


class CreateUser(BaseUser, PasswordScheme):
    pass


class UserRead(BaseUser):
    created_at: datetime

    class Config:
        from_attributes = True


class UserEmailOrUsername(BaseModel):
    email: EmailStr | None = None
    username: Annotated[str, MinLen(3), MaxLen(25)] | None = None

    @model_validator(mode="after")
    def check_email_or_username_provided(self):
        if not self.email and not self.username:
            raise ValueError("Neither email nor username provided")
        return self


class UserLogin(UserEmailOrUsername):
    password: Annotated[str, MinLen(8)]


class CodeScheme(BaseModel):
    code: int


class PasswordAndCodeScheme(PasswordScheme, CodeScheme):
    pass


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"
