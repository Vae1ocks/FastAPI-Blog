from dataclasses import dataclass
from typing import BinaryIO

from application.dto.other.file import FileDTO


@dataclass(frozen=True, slots=True)
class UserCreateDTO:
    username: str
    email: str
    password: str
    image: FileDTO | None = None
