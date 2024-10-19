from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from src.config import settings
from src.auth.views.reg_views import router as reg_router
from src.auth.views.auth_views import router as auth_router

import uvicorn


app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=settings.session.secret)
app.include_router(reg_router)
app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
