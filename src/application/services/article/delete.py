from dataclasses import dataclass

from application.errors.common.not_found import DoesNotExist
from domain.entities.article.models import Article, ArticleId
from domain.repositories.article_repository import ArticleRepository


@dataclass
class ArticleDeleteService:
    article_repository: ArticleRepository

    async def __call__(self, article_id: ArticleId) -> Article:
        article: Article | None = await self.article_repository.get_by_id(
            article_id=article_id
        )
        if article is None:
            raise DoesNotExist(obj_name="Article", obj_id=article_id)

        await self.article_repository.delete(article)
        return article
