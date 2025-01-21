from pydantic import BaseModel


class UserReadScheme(BaseModel):
    id: int
    username: str
    is_active: bool
    is_superuser: bool
    email: str | None = None


class UserListScheme(BaseModel):
    id: int
    username: str
