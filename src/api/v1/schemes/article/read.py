from datetime import datetime

from pydantic import BaseModel

from api.v1.schemes.comment.read import CommentReadScheme
from api.v1.schemes.user.user_read import UserListScheme
from domain.entities.article.models import ArticleStatus


class ArticleReadScheme(BaseModel):
    id: int
    title: str
    body: str
    status: str
    created_at: datetime
    updated_at: datetime | None
    author: UserListScheme
    comments: list[CommentReadScheme]


class ArticleListScheme(BaseModel):
    id: int
    author: UserListScheme
    title: str
    status: ArticleStatus
    created_at: datetime
    updated_at: datetime | None = None

