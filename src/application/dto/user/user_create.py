from dataclasses import dataclass
from typing import BinaryIO


@dataclass(frozen=True, slots=True)
class UserCreateDTO:
    username: str
    email: str
    password: str
    image: BinaryIO | None = None
