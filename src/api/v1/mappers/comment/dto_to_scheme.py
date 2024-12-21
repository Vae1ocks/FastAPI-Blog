from api.v1.mappers.user.dto_to_scheme import UserDTOToSchemeMapper
from api.v1.schemes.comment.read import CommentReadScheme
from application.dto.comment.comment_read import CommentReadDTO


class CommentDTOToSchemeMapper:
    @staticmethod
    def to_read_scheme(dto: CommentReadDTO) -> CommentReadScheme:
        author = UserDTOToSchemeMapper.to_list_scheme(dto=dto.author)
        return CommentReadScheme(
            id=dto.id,
            body=dto.body,
            author=author,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
        )
