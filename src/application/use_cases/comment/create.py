import logging
from dataclasses import dataclass

from application.dto.comment.comment_create import CommentCreateDTO
from application.dto.comment.comment_read import CommentReadDTO
from application.mappers.comment.model_to_dto import CommentModelToDTOMapper
from application.services.comment.create import CommentCreateService
from domain.entities.comment.models import Comment
from domain.entities.user.models import UserId
from infrastructure.managers.jwt import JWTTokenManager

logger = logging.getLogger(__name__)


@dataclass
class CommentCreateUseCase:
    create_service: CommentCreateService
    jwt_token_manager: JWTTokenManager

    async def execute(self, dto: CommentCreateDTO) -> CommentReadDTO:
        logger.debug("CommentCreateUseCase: started")
        user_id: UserId = self.jwt_token_manager.get_subject_id_from_request_token()
        total_dto: CommentCreateDTO = CommentCreateDTO(
            article_id=dto.article_id,
            body=dto.body,
            author_id=user_id,
        )
        comment: Comment = await self.create_service(dto=total_dto)
        read_dto: CommentReadDTO = CommentModelToDTOMapper.to_read_dto(model=comment)
        logger.debug("CommentCreateUseCase: finished")
        return read_dto
