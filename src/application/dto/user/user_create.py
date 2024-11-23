from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class UserCreateDTO:
    username: str
    email: str
    password: str
    image_path: str | None = None
