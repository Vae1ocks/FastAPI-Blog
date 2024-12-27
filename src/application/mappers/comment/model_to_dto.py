from application.dto.comment.comment_read import CommentReadDTO
from application.mappers.user.user_to_dto import UserToDTOMapper
from domain.entities.comment.models import Comment


class CommentModelToDTOMapper:
    @staticmethod
    def to_read_dto(model: Comment) -> CommentReadDTO:
        author = UserToDTOMapper.to_list_dto(user=model.author)
        return CommentReadDTO(
            id=model.id,
            body=model.body,
            author=author,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
