from dataclasses import dataclass

from application.commiter import Commiter
from application.dto.comment.comment_read import CommentReadDTO
from application.dto.comment.comment_update import CommentUpdateDTO
from application.errors.common.no_permission import NoPermissionError
from application.mappers.comment.model_to_dto import CommentModelToDTOMapper
from application.services.comment.update import CommentUpdateService
from domain.entities.comment.models import Comment
from domain.entities.user.models import UserId
from infrastructure.managers.jwt import JWTTokenManager


@dataclass
class CommentUpdateUseCase:
    update_service: CommentUpdateService
    commiter: Commiter
    jwt_token_manager: JWTTokenManager

    async def execute(self, dto: CommentUpdateDTO) -> CommentReadDTO:
        user_id: UserId = self.jwt_token_manager.get_subject_id_from_request_token()
        comment: Comment = await self.update_service(dto=dto)
        if comment.author_id != user_id:
            raise NoPermissionError()

        await self.commiter.commit()
        return CommentModelToDTOMapper.to_read_dto(model=comment)
