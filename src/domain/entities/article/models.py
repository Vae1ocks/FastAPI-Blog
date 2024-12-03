from dataclasses import dataclass, field
from enum import StrEnum, auto
from datetime import datetime, UTC
from functools import partial
from typing import NewType, TYPE_CHECKING

from .value_objects import ArticleTitle, ArticleBody

if TYPE_CHECKING:
    from ..user.models import UserId
    from ..comment.models import CommentId

ArticleId = NewType("ArticleId", int)

UTC_NOW = partial(datetime.now, UTC)


class ArticleStatus(StrEnum):
    draft = auto()
    published = auto()


@dataclass
class Article:
    id: ArticleId
    title: ArticleTitle
    body: ArticleBody
    status: ArticleStatus
    created_at: datetime = field(default_factory=UTC_NOW, kw_only=True)
    updated_at: datetime
    author_id: "UserId"
    comments_id: "CommentId"
