from typing import AsyncIterable

from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)

from setup.configs import AllConfigs


class DatabaseProvider(Provider):
    @provide(scope=Scope.APP)
    async def provide_async_engine(
        self,
        configs: AllConfigs,
    ) -> AsyncIterable[AsyncEngine]:
        async_engine_params = {"url": configs.db.url, **configs.sqla_eng.model_dump()}
        async_engine = create_async_engine(**async_engine_params)
        yield async_engine
        await async_engine.dispose()

    @provide(scope=Scope.APP)
    def provide_async_session_maker(
        self,
        async_engine: AsyncEngine,
        configs: AllConfigs
    ) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(bind=async_engine, **configs.sqla_sess.model_dump())

    @provide(scope=Scope.REQUEST, provides=AsyncSession)
    async def provide_async_session(
        self, async_session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AsyncSession]:
        async with async_session_maker() as session:
            yield session
