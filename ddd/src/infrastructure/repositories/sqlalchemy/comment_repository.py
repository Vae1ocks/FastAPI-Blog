from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.comment.models import Comment, CommentId
from domain.entities.article.models import ArticleId


class CommentRepositoryImpl:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, comment_id: CommentId) -> Comment | None:
        stmt = select(Comment).where(Comment.id == comment_id)
        result = (await self.session.execute(stmt)).scalar_one_or_none()
        return result

    async def get_by_article(self, article_id: ArticleId) -> list[Comment]:
        stmt = select(Comment).where(Comment.article_id == article_id)
        result = (await self.session.execute(stmt)).scalars()
        return list(result.all())

    async def add(self, comment: Comment) -> None:
        self.session.add(comment)

    async def delete(self, comment_id: Comment) -> None:
        stmt = select(Comment).where(Comment.id == comment_id)
        comment = (await self.session.execute(stmt)).scalar_one_or_none()
        if comment is None:
            raise ValueError(f"Comment with id={comment_id} does not exist.")
        await self.session.delete(comment)
