from dataclasses import dataclass
from datetime import datetime

from domain.entities.article.models import ArticleStatus
from ..user.user_read import UserListDTO
from ..comment.comment_read import CommentReadDTO


@dataclass(frozen=True, slots=True)
class ArticleReadDTO:
    id: int
    title: str
    body: str
    status: str
    created_at: datetime
    updated_at: datetime
    author: UserListDTO
    comments: list[CommentReadDTO]


@dataclass(frozen=True, slots=True)
class ArticleListDTO:
    id: int
    user: UserListDTO
    title: str
    body: str
    created_at: datetime
    status: ArticleStatus | None = None
    updated_at: datetime | None = None
