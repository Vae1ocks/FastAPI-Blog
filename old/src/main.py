from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from old.src.config import settings
from old.src.auth.views.reg_views import router as reg_router
from old.src.auth.views.auth_views import router as auth_router
from old.src.users.views import router as users_router
from old.src.articles.views import router as articles_router

import uvicorn


app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=settings.session.secret)
app.include_router(reg_router)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(articles_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
