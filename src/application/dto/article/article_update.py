from dataclasses import dataclass

from domain.entities.article.models import ArticleStatus, ArticleTitle, ArticleBody, ArticleId


@dataclass(frozen=True, slots=True)
class ArticleUpdateDTO:
    id: ArticleId
    title: ArticleTitle | None = None
    body: ArticleBody | None = None
    status: ArticleStatus | None = None
