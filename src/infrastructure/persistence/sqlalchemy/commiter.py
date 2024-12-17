from sqlalchemy.ext.asyncio import AsyncSession

from application.commiter import Commiter


class SqlaCommiter(Commiter):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def commit(self) -> None:
        await self.session.commit()

    async def flush(self) -> None:
        await self.session.flush()
