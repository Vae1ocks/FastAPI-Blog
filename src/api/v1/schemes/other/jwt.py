from pydantic import BaseModel


class JWTTokenScheme(BaseModel):
    access: str
    refresh: str
