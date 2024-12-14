from typing import AsyncIterable

from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)

from infrastructure.persistence.config import (
    SqlaEngineConfig,
    DatabaseConfig,
    SqlaSessionConfig,
)


class DatabaseProvider(Provider):
    @provide
    async def provide_async_engine(
        self,
        db_settings: DatabaseConfig,
        engine_config: SqlaEngineConfig,
    ) -> AsyncIterable[AsyncEngine]:
        async_engine_params = {"url": db_settings.url, **engine_config.model_dump()}
        async_engine = create_async_engine(**async_engine_params)
        yield async_engine
        await async_engine.dispose()

    @provide(scope=Scope.APP)
    def provide_async_session_maker(
        self,
        async_engine: AsyncEngine,
        session_settings: SqlaSessionConfig,
    ) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(bind=async_engine, **session_settings.model_dump())

    @provide(scope=Scope.REQUEST)
    async def provide_async_session(
        self,
        async_session_maker: async_sessionmaker[AsyncSession],
    ) -> AsyncIterable[AsyncSession]:
        async with async_session_maker() as session:
            yield session
