from typing import BinaryIO

from pydantic import BaseModel


class UserCreateScheme(BaseModel):
    username: str
    email: str
    password: str
    image: BinaryIO | None = None

    class Config:
        arbitrary_types_allowed = True
