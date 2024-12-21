from pydantic import BaseModel

from domain.entities.article.models import ArticleStatus


class ArticleCreateScheme(BaseModel):
    title: str
    body: str
    status: ArticleStatus
