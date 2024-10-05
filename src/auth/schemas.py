from typing import Annotated

from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, EmailStr, ConfigDict


class BaseUser(BaseModel):
    email: EmailStr
    username: Annotated[str, MinLen(3), MaxLen(25)]

class CreateUser(BaseUser):
    password: Annotated[str, MinLen(8)]


class UserRead(BaseUser):
    pass