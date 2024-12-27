from dataclasses import dataclass

from domain.entities.article.models import ArticleId
from domain.entities.comment.value_objects import CommentBody
from domain.entities.user.models import UserId


@dataclass(frozen=True, slots=True)
class CommentCreateDTO:
    article_id: ArticleId
    body: CommentBody
    author_id: UserId | None = None
