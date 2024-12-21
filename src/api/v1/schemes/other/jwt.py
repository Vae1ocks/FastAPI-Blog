from pydantic import BaseModel


class JWTTokenScheme(BaseModel):
    access: str | bytes
    refresh: str | bytes


class JWTAccessScheme(BaseModel):
    access: str | bytes


class JWTRefreshScheme(BaseModel):
    refresh: str | bytes
