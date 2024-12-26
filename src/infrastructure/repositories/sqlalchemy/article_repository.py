from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from domain.entities.article.models import Article, ArticleId, ArticleStatus


class ArticleRepositoryImpl:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self, limit: int, offset: int) -> list[Article | None]:
        stmt = select(Article).limit(limit).offset(offset)
        result = await self.session.scalars(stmt)
        return list(result.all())

    async def get_by_id(self, article_id: ArticleId) -> Article | None:
        stmt = (
            select(Article)
            .where(Article.id == article_id)  # noqa
            .where(Article.id == article_id)
            .options(joinedload(Article.comments), joinedload(Article.author))  # noqa
        )
        return (await self.session.execute(stmt)).unique().scalar_one_or_none()

    async def get_by_status(
        self,
        status: ArticleStatus,
        limit: int,
        offset: int,
    ) -> list[Article | None]:
        stmt = (
            select(Article).where(Article.status == status).limit(limit).offset(offset)
        )
        return list((await self.session.scalars(stmt)).all())

    def add(self, article: Article) -> None:
        self.session.add(article)

    async def delete(self, article: Article) -> None:
        await self.session.delete(article)
