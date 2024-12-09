from pydantic import BaseModel


class LoginScheme(BaseModel):
    username: str
    password: str
