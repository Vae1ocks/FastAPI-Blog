from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from fastapi_users.db import SQLAlchemyBaseUserTable

from src.models import Base

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class User(Base, SQLAlchemyBaseUserTable[int]):
    @classmethod
    def get_db(cls, session: AsyncSession):
        return SQLAlchemyUserDatabase(session, cls)
