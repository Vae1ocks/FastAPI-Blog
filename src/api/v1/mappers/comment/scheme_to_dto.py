from api.v1.schemes.comment.create import CommentCreateScheme
from api.v1.schemes.comment.update import CommentUpdateScheme
from application.dto.comment.comment_create import CommentCreateDTO
from application.dto.comment.comment_update import CommentUpdateDTO
from domain.entities.article.models import ArticleId
from domain.entities.comment.models import CommentId
from domain.entities.comment.value_objects import CommentBody


class CommentSchemeToDTOMapper:
    @staticmethod
    def to_create_dto(
        scheme: CommentCreateScheme, article_id: ArticleId
    ) -> CommentCreateDTO:
        return CommentCreateDTO(
            article_id=article_id,
            body=CommentBody(scheme.body),
            author_id=None,
        )

    @staticmethod
    def to_update_dto(
        scheme: CommentUpdateScheme, comment_id: CommentId
    ) -> CommentUpdateDTO:
        return CommentUpdateDTO(
            id=comment_id,
            body=CommentBody(scheme.body),
        )
