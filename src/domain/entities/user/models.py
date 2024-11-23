from dataclasses import dataclass
from datetime import datetime
from typing import NewType

UserId = NewType("UserId", int)


@dataclass
class User:
    id: UserId
    email: str
    username: str
    password: str
    created_at: datetime
    image_path: str | None = None
    is_active: bool = True
    is_confirmed: bool = False
    is_superuser: bool = False
