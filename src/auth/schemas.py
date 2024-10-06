from typing import Annotated

from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, EmailStr, ConfigDict, model_validator


class BaseUser(BaseModel):
    email: EmailStr
    username: Annotated[str, MinLen(3), MaxLen(25)]


class CreateUser(BaseUser):
    password: Annotated[str, MinLen(8)]


class UserRead(BaseUser):
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr | None = None
    username: Annotated[str, MinLen(3), MaxLen(25)] | None = None
    password: Annotated[str, MinLen(8)]

    @model_validator(mode="after")
    def check_email_or_username_provided(self):
        if not self.email and not self.username:
            raise ValueError("Neither email nor username provided")
        return self


class Code(BaseModel):
    code: int
