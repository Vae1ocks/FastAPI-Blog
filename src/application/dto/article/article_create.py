from dataclasses import dataclass

from domain.entities.article.models import ArticleStatus, ArticleTitle, ArticleBody
from domain.entities.user.models import UserId


@dataclass(frozen=True, slots=True)
class ArticleCreateDTO:
    author_id: UserId
    title: ArticleTitle
    body: ArticleBody
    status: ArticleStatus
