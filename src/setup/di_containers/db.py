from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Resource

from infrastructure.persistence.database import get_async_engine, get_async_sessionmaker
from infrastructure.persistence.uow import SQLAUnitOfWork
from setup.configs import configs


class DbContainer(DeclarativeContainer):
    engine = Resource(
        get_async_engine,
        pg_dsn=configs.db.url,
        settings=configs.sqla_eng,
    )
    session_maker = Factory(
        get_async_sessionmaker,
        engine=engine,
        settings=configs.sqla_sess,
    )
    uow = Factory(
        SQLAUnitOfWork, session_maker=session_maker
    )
