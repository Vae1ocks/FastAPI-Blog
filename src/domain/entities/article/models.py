from dataclasses import dataclass, field
from enum import StrEnum, auto
from datetime import datetime, UTC
from functools import partial
from typing import NewType, TYPE_CHECKING, Optional

from .value_objects import ArticleTitle, ArticleBody

if TYPE_CHECKING:
    from ..user.models import UserId, User
    from ..comment.models import CommentId, Comment

ArticleId = NewType("ArticleId", int)

UTC_NOW = partial(datetime.now, UTC)


@dataclass
class ArticleStatus(StrEnum):
    draft = auto()
    published = auto()

    def __hash__(self):
        return hash(self.value)


@dataclass(kw_only=True)
class Article:
    id: ArticleId | None = None
    title: ArticleTitle
    body: ArticleBody
    status: ArticleStatus
    created_at: datetime = field(default_factory=UTC_NOW, kw_only=True)
    author_id: "UserId"
    comments_id: Optional["CommentId"] = None
    updated_at: datetime | None = None
    author: "User | None" = field(init=False)
    comments: list["Comment"] = field(default_factory=list)
