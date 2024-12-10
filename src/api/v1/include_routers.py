from fastapi import FastAPI

from .endpoints.user.registration import router as user_reg_router
from .endpoints.user.authentication import router as auth_router


def include_routers(app: FastAPI) -> None:
    app.include_router(user_reg_router)
    app.include_router(auth_router)
