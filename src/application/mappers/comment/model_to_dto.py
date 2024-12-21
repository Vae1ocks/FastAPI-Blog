from application.dto.comment.comment_read import CommentReadDTO
from application.mappers.user.user_to_dto import UserToDTOMapper
from domain.entities.comment.models import Comment


class CommentToDTOMapper:
    @staticmethod
    def to_list_dto(comment: Comment) -> CommentReadDTO:
        author = UserToDTOMapper.to_list_dto(user=comment.author)
        return CommentReadDTO(
            id=comment.id,
            body=str(comment.body),
            author=author,
            created_at=comment.created_at,
            updated_at=comment.updated_at,
        )
