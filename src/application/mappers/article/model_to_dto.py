from application.dto.article.article_read import ArticleReadDTO
from application.mappers.comment.model_to_dto import CommentToDTOMapper
from application.mappers.user.user_to_dto import UserToDTOMapper
from domain.entities.article.models import Article


class ArticleModelToDTOMapper:
    @staticmethod
    def to_read_dto(model: Article) -> ArticleReadDTO:
        user_dto = UserToDTOMapper.to_list_dto(user=Article.author)
        comments_dtos = []
        for comment in Article.comments:
            comments_dtos.append(CommentToDTOMapper.to_list_dto(comment=comment))
        return ArticleReadDTO(
            id=model.id,
            author=user_dto,
            title=str(model.title),
            body=str(model.body),
            status=str(model.status),
            created_at=model.created_at,
            updated_at=model.updated_at,
            comments=comments_dtos,
        )
