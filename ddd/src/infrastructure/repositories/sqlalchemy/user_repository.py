from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.user.models import User, UserId


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: UserId) -> User | None:
        stmt = select(User).where(User.id == user_id)
        return (await self.session.execute(stmt)).scalar_one_or_none()

    async def get_by_username(self, username: str, status: str | None) -> User:
        stmt = select(User).where(
            User.username == username, User.status == status
        )
        return (await self.session.execute(stmt)).scalar_one_or_none()

    async def get_by_email(self, email: str, status: str | None) -> User:
        stmt = select(User).where(
            User.email == email, User.status == status
        )
        return (await self.session.execute(stmt)).scalar_one_or_none()

    async def add(self, user: User) -> None:
        self.session.add(user)

    async def delete(self, user_id: UserId) -> None:
        stmt = select(User).where(User.id == user_id)
        user = (await self.session.execute(stmt)).scalar_one_or_none()
        if user is None:
            raise ValueError(f"User with id={user_id} does not exist.")
        await self.session.delete(user)
