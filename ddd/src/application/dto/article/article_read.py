from dataclasses import dataclass
from datetime import datetime

from domain.entities.article.models import ArticleStatus
from ..user.user_read import UserListDTO
from ..comment.comment_read import CommentListDTO


dataclass(frozen=True, slots=True)
class ArticleReadDTO:
    id: int
    user: UserListDTO
    title: str
    body: str
    status: ArticleStatus | None = None
    created_at: datetime
    updated_at: datetime | None = None
    comments: list[CommentListDTO]


@dataclass(frozen=True, slots=True)
class ArticleListDTO:
    id: int
    user: UserListDTO
    title: str
    body: str
    created_at: datetime
    status: ArticleStatus | None = None
    updated_at: datetime | None = None
