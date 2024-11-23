from typing import Protocol, List

from domain.entities.article.models import Article, ArticleId, ArticleStatus


class ArticleRepository(Protocol):
    async def get_all(self, limit: int, offset: int) -> List[Article | None]:
        ...

    async def get_by_id(self, article_id: ArticleId) -> Article | None:
        ...

    async def get_by_status(self, status: ArticleStatus, limit: int, offset: int) -> List[Article | None]:
        ...

    async def add(self, values: dict) -> Article:
        ...

    async def delete(self, article: Article) -> None:
        ...
