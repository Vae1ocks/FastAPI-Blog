from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_users.db import SQLAlchemyBaseUserTable

from src.models import Base


class User(Base, SQLAlchemyBaseUserTable[int]):
    pass
