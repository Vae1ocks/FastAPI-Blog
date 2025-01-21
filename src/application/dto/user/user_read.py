from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class UserReadDTO:
    id: int
    username: str
    is_active: bool
    is_superuser: bool
    email: str | None = None


@dataclass(frozen=True, slots=True)
class UserListDTO:
    id: int
    username: str
