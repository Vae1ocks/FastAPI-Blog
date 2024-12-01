import uvicorn
from fastapi import FastAPI

from setup.app_factory import create_app
from setup.configs import configs

app: FastAPI = create_app()


if __name__ == "__main__":
    uvicorn.run(
        app=app,
        host=configs.uvicorn.host,
        port=configs.uvicorn.port,
        reload=configs.uvicorn.reload,
    )
