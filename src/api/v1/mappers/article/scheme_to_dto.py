from api.v1.schemes.article.create import ArticleCreateScheme
from api.v1.schemes.article.update import ArticleUpdateScheme
from application.dto.article.article_create import ArticleCreateDTO
from application.dto.article.article_update import ArticleUpdateDTO
from domain.entities.article.models import ArticleStatus
from domain.entities.article.value_objects import ArticleTitle, ArticleBody


class ArticleSchemeToDTOMapper:
    @staticmethod
    def to_create_dto(scheme: ArticleCreateScheme) -> ArticleCreateDTO:
        return ArticleCreateDTO(
            author_id=None,
            title=ArticleTitle(value=scheme.title),
            body=ArticleBody(value=scheme.body),
            status=ArticleStatus(scheme.status),
        )

    @staticmethod
    def to_update_dto(scheme: ArticleUpdateScheme) -> ArticleUpdateDTO:
        return ArticleUpdateDTO(
            id=scheme.id,
            title=ArticleTitle(scheme.title),
            body=ArticleBody(scheme.body),
            status=scheme.status,
        )
