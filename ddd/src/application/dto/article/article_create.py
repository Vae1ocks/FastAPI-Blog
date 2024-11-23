from dataclasses import dataclass

from domain.entities.article.models import ArticleStatus, ArticleTitle, ArticleBody


@dataclass(frozen=True, slots=True)
class ArticleCreateDTO:
    user_id: str
    title: ArticleTitle
    body: ArticleBody
    status: ArticleStatus
