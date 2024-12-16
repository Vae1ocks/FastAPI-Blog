from contextlib import asynccontextmanager
from typing import AsyncIterator

from dishka import AsyncContainer
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from api.v1.exception_handler import ExceptionMessageProvider, ExceptionMapper, ExceptionHandler
from api.v1.include_routers import include_routers
from infrastructure.persistence.sqlalchemy.models import map_tables
from setup.configs import AllConfigs


# from setup.di_containers.main import MainContainer
# from setup.di_containers.setup import setup_container
# from .ioc.setup import create_async_ioc_container, get_providers


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    yield None
    await app.state.dishka_container.close()  # noqa


def configure_app(app: FastAPI, configs: AllConfigs) -> None:
    app.add_middleware(SessionMiddleware, secret_key=configs.session.secret)  # noqa
    include_routers(app)
    exception_message_provider: ExceptionMessageProvider = ExceptionMessageProvider()
    exception_mapper: ExceptionMapper = ExceptionMapper()
    exception_handler: ExceptionHandler = ExceptionHandler(
        app=app,
        exception_message_provider=exception_message_provider,
        mapper=exception_mapper,
    )
    exception_handler.setup_handlers()


def create_app(configs: AllConfigs) -> FastAPI:
    # container = setup_container(modules=["api.v1"])
    map_tables()
    app = FastAPI(
        title="FastAPI Blog",
        docs_url="/api/docs",
        debug=True,
        lifespan=lifespan
    )
    configure_app(app=app, configs=configs)
    return app
