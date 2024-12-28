from dataclasses import dataclass

from application.errors.common.not_found import DoesNotExist
from domain.entities.comment.models import CommentId, Comment
from domain.repositories.comment_repository import CommentRepository


@dataclass
class CommentDeleteService:
    comment_repository: CommentRepository

    async def __call__(self, comment_id: CommentId) -> Comment:
        comment: Comment | None = await self.comment_repository.get_by_id(comment_id)
        if comment is None:
            raise DoesNotExist(obj_name="Comment", obj_id=comment_id)

        await self.comment_repository.delete(comment)
        return comment