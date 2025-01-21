from fastapi import UploadFile
from pydantic import BaseModel, Field


class UserCreateScheme(BaseModel):
    username: str = Field(max_length=25)
    email: str
    password: str
    image: UploadFile | None = None

    class Config:
        arbitrary_types_allowed = True
