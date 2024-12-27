from typing import Protocol, List

from application.common.enums.sort_order import SortOrder
from domain.entities.article.models import Article, ArticleId, ArticleStatus


class ArticleRepository(Protocol):
    async def get_list(
        self, offset: int, limit: int, order: SortOrder
    ) -> List[Article | None]: ...

    async def get_by_id(self, article_id: ArticleId) -> Article | None: ...

    async def get_by_status(
        self, status: ArticleStatus, limit: int, offset: int
    ) -> List[Article | None]: ...

    def add(self, article: Article) -> None: ...

    async def delete(self, article: Article) -> None: ...
