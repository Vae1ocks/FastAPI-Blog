from typing import Protocol, List

from domain.entities.comment.models import Comment, CommentId
from domain.entities.article.models import Article


class CommentRepository(Protocol):
    async def get_by_id(self, comment_id: CommentId) -> Comment | None:
        ...

    async def get_by_article(self, article: Article) -> List[Comment | None]:
        ...

    def add(self, comment: Comment) -> None:
        ...

    async def delete(self, comment: Comment) -> None:
        ...
