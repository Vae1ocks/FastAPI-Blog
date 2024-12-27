from fastapi import FastAPI

from .endpoints.user.registration import router as user_reg_router
from .endpoints.user.authentication import router as auth_router
from .endpoints.article.router import router as article_router
from .endpoints.comment.router import router as comment_router



def include_routers(app: FastAPI) -> None:
    app.include_router(user_reg_router)
    app.include_router(auth_router)
    app.include_router(article_router)
    app.include_router(comment_router)
