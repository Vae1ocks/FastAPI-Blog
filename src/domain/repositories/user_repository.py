from typing import Protocol

from domain.entities.user.models import User, UserId


class UserRepository(Protocol):
    async def get_by_id(self, user_id: UserId) -> User | None: ...

    async def get_by_username(
        self,
        username: str,
        is_active: bool | None = None,
        is_confirmed: bool | None = None,
    ) -> User: ...

    async def get_by_email(
        self,
        email: str,
        is_active: bool | None = None,
        is_confirmed: bool | None = None,
    ) -> User: ...

    async def get_by_email_or_username(
        self,
        email: str,
        username: str,
        is_active: bool | None = None,
        is_confirmed: bool | None = None,
    ) -> list[User]: ...

    def add(self, user: User) -> None: ...

    async def delete(self, user: User) -> None: ...
