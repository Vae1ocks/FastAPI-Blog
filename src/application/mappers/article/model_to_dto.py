from application.dto.article.article_read import ArticleReadDTO, ArticleListDTO
from application.dto.user.user_read import UserListDTO
from application.mappers.comment.model_to_dto import CommentToDTOMapper
from application.mappers.user.user_to_dto import UserToDTOMapper
from domain.entities.article.models import Article


class ArticleModelToDTOMapper:
    @staticmethod
    def to_read_dto(model: Article) -> ArticleReadDTO:
        user_dto = UserToDTOMapper.to_list_dto(user=model.author)
        comments_dtos = []
        for comment in model.comments:
            comments_dtos.append(CommentToDTOMapper.to_list_dto(comment=comment))
        return ArticleReadDTO(
            id=model.id,
            author=user_dto,
            title=model.title,
            body=model.body,
            status=model.status,
            created_at=model.created_at,
            updated_at=model.updated_at,
            comments=comments_dtos,
        )

    @staticmethod
    def to_list_dtos(models: list[Article | None]):
        dtos = []
        for article in models:
            if article is None:
                break
            user: UserListDTO = UserToDTOMapper.to_list_dto(user=article.author)
            dto: ArticleListDTO = ArticleListDTO(
                id=article.id,
                author=user,
                title=article.title,
                created_at=article.created_at,
                status=article.status,
                updated_at=article.updated_at,
            )
            dtos.append(dto)
        return dtos
