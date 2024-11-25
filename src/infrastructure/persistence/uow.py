from dataclasses import dataclass

from application.uow import UnitOfWork
from infrastructure.repositories.sqlalchemy.user_repository import UserRepositoryImpl
from infrastructure.repositories.sqlalchemy.article_repository import ArticleRepositoryImpl
from infrastructure.repositories.sqlalchemy.comment_repository import CommentRepositoryImpl
from .database import database


@dataclass
class SQLAUnitOfWork(UnitOfWork):
    def __init__(self, session_factory):
        self._session_factory = session_factory
        self._user_repository = None
        self._article_repository = None
        self._comment_repository = None

    async def __aenter__(self):
        self.session = self._session_factory()
        return self

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

    @property
    def user_repository(self):
        if self._user_repository is None:
            self._user_repository = UserRepositoryImpl(session=self.session)
        return self._user_repository

    @property
    def article_repository(self):
        if self._article_repository is None:
            self._article_repository = ArticleRepositoryImpl(session=self.session)
        return self._article_repository

    @property
    def comment_repository(self):
        if self._comment_repository is None:
            self._comment_repository = CommentRepositoryImpl(session=self.session)
        return self._comment_repository
