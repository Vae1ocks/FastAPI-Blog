from dataclasses import dataclass, field
from datetime import datetime, UTC
from functools import partial
from typing import NewType, TYPE_CHECKING

from .value_objects import CommentBody

if TYPE_CHECKING:
    from ..article.models import ArticleId
    from ..user.models import UserId

CommentId = NewType("CommentId", int)

UTC_NOW = partial(datetime.now, UTC)


@dataclass
class Comment:
    id: CommentId
    body: CommentBody
    created_at: datetime = field(default_factory=UTC_NOW, kw_only=True)
    updated_at: datetime
    article_id: "ArticleId"
    author_id: "UserId"
