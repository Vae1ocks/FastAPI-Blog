from sqlalchemy import select, Select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.user.models import User, UserId


def add_is_conf_is_active_to_stmt(
    stmt: Select,
    is_active: bool,
    is_confirmed: bool,
):
    if is_active is not None:
        stmt = stmt.where(User.is_active == is_active)  # type: ignore
    if is_confirmed is not None:
        stmt = stmt.where(User.is_confirmed == is_confirmed)  # type: ignore
    return stmt


class UserRepositoryImpl:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: UserId) -> User | None:
        stmt = select(User).where(User.id == user_id)  # type: ignore
        return (await self.session.execute(stmt)).scalar_one_or_none()

    async def get_by_username(
        self,
        username: str,
        is_active: bool | None = None,
        is_confirmed: bool | None = None,
    ) -> User:
        stmt = select(User).where(User.username == username)  # type: ignore
        stmt = add_is_conf_is_active_to_stmt(
            stmt=stmt, is_active=is_active, is_confirmed=is_confirmed
        )
        return (await self.session.execute(stmt)).scalar_one_or_none()

    async def get_by_email(
        self,
        email: str,
        is_active: bool | None = None,
        is_confirmed: bool | None = None,
    ) -> User:
        stmt = select(User).where(User.email == email)  # type: ignore
        stmt = add_is_conf_is_active_to_stmt(
            stmt=stmt, is_active=is_active, is_confirmed=is_confirmed
        )
        return (await self.session.execute(stmt)).scalar_one_or_none()

    async def get_by_email_or_username(
        self,
        email: str,
        username: str,
        is_active: bool | None = None,
        is_confirmed: bool | None = None,
    ) -> list[User]:
        stmt = select(User).where(
            (User.email == email) | (User.username == username)  # type: ignore
        )
        stmt = add_is_conf_is_active_to_stmt(
            stmt=stmt, is_active=is_active, is_confirmed=is_confirmed
        )
        return list((await self.session.execute(stmt)).scalars())

    def add(self, user: User) -> None:
        self.session.add(user)

    async def delete(self, user_id: UserId) -> None:
        stmt = select(User).where(User.id == user_id)  # type: ignore
        user = (await self.session.execute(stmt)).scalar_one_or_none()
        if user is None:
            raise ValueError(f"User with id={user_id} does not exist.")
        await self.session.delete(user)
