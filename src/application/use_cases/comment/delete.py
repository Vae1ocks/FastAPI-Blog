import logging
from dataclasses import dataclass

from application.commiter import Commiter
from application.errors.common.no_permission import NoPermissionError
from application.services.comment.delete import CommentDeleteService
from domain.entities.comment.models import CommentId, Comment
from domain.entities.user.models import UserId
from infrastructure.managers.jwt import JWTTokenManager

logger = logging.getLogger(__name__)


@dataclass
class CommentDeleteUseCase:
    delete_service: CommentDeleteService
    jwt_token_manager: JWTTokenManager
    commiter: Commiter

    async def execute(self, comment_id: CommentId) -> None:
        logger.debug("Executing CommentDeleteUseCase: started")
        user_id: UserId = self.jwt_token_manager.get_subject_id_from_request_token()
        comment: Comment = await self.delete_service(comment_id=comment_id)
        if comment.author_id != user_id:
            logger.debug("CommentDeleteUseCase: NoPermissionError (author_id != user_id)")
            raise NoPermissionError()
        await self.commiter.commit()
        logger.debug("Executing CommentDeleteUseCase: finished with commit")
