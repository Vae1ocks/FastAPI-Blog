from api.v1.schemes.article.create import ArticleCreateScheme
from application.dto.article.article_create import ArticleCreateDTO
from domain.entities.article.models import ArticleStatus
from domain.entities.article.value_objects import ArticleTitle, ArticleBody
from domain.entities.user.models import UserId


class ArticleSchemeToDTOMapper:
    @staticmethod
    def to_create_dto(scheme: ArticleCreateScheme) -> ArticleCreateDTO:
        return ArticleCreateDTO(
            author_id=None,
            title=ArticleTitle(title=scheme.title),
            body=ArticleBody(text=scheme.body),
            status=ArticleStatus(scheme.status),
        )
