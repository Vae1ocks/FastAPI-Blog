import logging
from dataclasses import dataclass

from application.commiter import Commiter
from application.dto.comment.comment_create import CommentCreateDTO
from domain.entities.comment.models import Comment
from domain.exceptions.base import DomainFieldError
from domain.repositories.comment_repository import CommentRepository

logger = logging.getLogger(__name__)


@dataclass
class CommentCreateService:
    comment_repository: CommentRepository
    commiter: Commiter

    async def __call__(self, dto: CommentCreateDTO) -> Comment:
        if dto.author_id is None:
            logger.error("ArticleDTO.author_id is None")
            raise DomainFieldError()

        comment = Comment(
            body=dto.body,
            article_id=dto.article_id,
            author_id=dto.author_id,
        )
        self.comment_repository.add(comment)
        await self.commiter.commit()
        logger.debug("CommentCreateService: commit")
        comment: Comment = await self.comment_repository.get_by_id(comment.id)
        return comment
