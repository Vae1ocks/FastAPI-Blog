from dataclasses import dataclass
from io import BytesIO


@dataclass(frozen=True, slots=True)
class UserCreateDTO:
    username: str
    email: str
    password: str
    image: BytesIO | None = None
