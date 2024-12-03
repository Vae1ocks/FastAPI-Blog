from dataclasses import dataclass
from datetime import datetime
from typing import NewType

UserId = NewType("UserId", int)


@dataclass(kw_only=True)
class User:
    id: UserId | None = None
    email: str
    username: str
    password: str
    created_at: datetime | None = None
    image_path: str | None = None
    is_active: bool = True
    is_confirmed: bool = False
    is_superuser: bool = False

    def confirm_registration(self) -> None:
        if self.is_confirmed:
            raise ValueError("User is already confirmed")
        self.is_confirmed = True

    def active(self):
        if self.is_active:
            raise ValueError("User is already active")
        self.is_active = True

    def deactivate(self):
        if not self.is_active:
            raise ValueError("User is already inactive")
        self.is_active = False
