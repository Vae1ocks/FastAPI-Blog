import uvicorn
from dishka import AsyncContainer
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from setup.app_factory import create_app
from setup.configs import configs as all_configs, AllConfigs
from setup.ioc.setup import create_async_ioc_container, get_providers


def make_app(configs: AllConfigs = all_configs) -> FastAPI:
    app: FastAPI = create_app(configs=configs)
    async_ioc_container: AsyncContainer = create_async_ioc_container(
        providers=get_providers(),
        configs=configs,
    )
    setup_dishka(
        container=async_ioc_container,
        app=app,
    )
    return app


app = make_app()

if __name__ == "__main__":
    uvicorn.run(
        app="run:app",
        host=all_configs.uvicorn.host,
        port=all_configs.uvicorn.port,
        reload=all_configs.uvicorn.reload,
    )
