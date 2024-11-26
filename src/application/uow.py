from abc import ABC, abstractmethod


class UnitOfWork(ABC):
    @abstractmethod
    async def __aenter__(self):
        raise NotImplementedError()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError()

    @abstractmethod
    async def commit(self):
        raise NotImplementedError()

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def user_repository(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def article_repository(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def comment_repository(self):
        raise NotImplementedError()
