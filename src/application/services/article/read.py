from dataclasses import dataclass

from application.dto.common.list import ListObjectsDTO
from application.errors.common.not_found import DoesNotExist
from domain.entities.article.models import ArticleId, Article
from domain.repositories.article_repository import ArticleRepository


@dataclass
class ArticleReadService:
    article_repository: ArticleRepository

    async def read_by_id(self, article_id: ArticleId) -> Article:
        article: Article | None = await self.article_repository.get_by_id(article_id)
        if article is None:
            raise DoesNotExist(obj_name="Article", obj_id=article_id)
        return article

    async def read_list(self, dto: ListObjectsDTO) -> list[Article | None]:
        articles: list[Article | None] = await self.article_repository.get_list(
            offset=dto.paginator.offset,
            limit=dto.paginator.limit,
            order=dto.order,
        )
        return articles
