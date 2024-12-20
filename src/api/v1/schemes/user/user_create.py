from typing import BinaryIO

from pydantic import BaseModel, Field


class UserCreateScheme(BaseModel):
    username: str = Field(max_length=25)
    email: str
    password: str
    image: BinaryIO | None = None

    class Config:
        arbitrary_types_allowed = True
