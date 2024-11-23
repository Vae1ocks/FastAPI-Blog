from dataclasses import dataclass

from application.uow import AbstractUnitOfWork
from .database import database


@dataclass
class SQLAUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory):
        self._session_factory = session_factory

    async def __aenter__(self):
        self.session = self._session_factory()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()
        else:
            await self.session.commit()
        self.session.close()

    async def commit(self):
        self.session.commit()

    async def rollback(self):
        self.session.rollback()
