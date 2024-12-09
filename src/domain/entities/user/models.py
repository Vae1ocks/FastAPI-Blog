from dataclasses import dataclass
from datetime import datetime
from typing import NewType

from domain.entities.user.errors import UserAlreadyConfirmedError, UserAlreadyActiveError, UserAlreadyDeactivatedError

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
            raise UserAlreadyConfirmedError()
        self.is_confirmed = True

    def activate(self):
        if self.is_active:
            raise UserAlreadyActiveError()
        self.is_active = True

    def deactivate(self):
        if not self.is_active:
            raise UserAlreadyDeactivatedError()
        self.is_active = False
