from datetime import datetime

from pydantic import BaseModel, Field

from src.auth.schemas import UserRead
from .models import ArticleStatus


class CommentBase(BaseModel):
    body: str


class CommentCreate(CommentBase):
    article_id: int


class CommentRead(CommentBase):
    author: UserRead


class ArticleBase(BaseModel):
    title: str = Field(min_length=5, max_length=150)
    body: str
    status: ArticleStatus


class ArticleCreate(ArticleBase):
    pass


class ArticleList(ArticleBase):
    created_at: datetime
    updated_at: datetime | None
    author: UserRead


class ArticleRead(ArticleList):
    comments: list[CommentRead]
