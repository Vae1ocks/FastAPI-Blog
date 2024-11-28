from asyncio import current_task
from typing import AsyncGenerator, AsyncIterable

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    async_scoped_session, AsyncEngine, AsyncSession,
)

from .config import SqlaEngineConfig, SqlaSessionConfig


async def get_engine(pg_dsn: str, settings: SqlaEngineConfig) -> AsyncGenerator[AsyncEngine, None]:
    engine = create_async_engine(
        pg_dsn,
        **settings.model_dump()
    )
    yield engine
    await engine.dispose()


async def get_async_sessionmaker(
    engine: AsyncEngine,
    settings: SqlaSessionConfig
) -> async_sessionmaker[AsyncSession]:
    session_factory = async_sessionmaker(
        engine, **settings.model_dump()
    )
    return session_factory


async def get_async_session(
    session_factory: async_sessionmaker[AsyncSession]
) -> AsyncIterable[AsyncSession]:
    async with session_factory() as session:
        yield session
