from application.dto.article.article_create import ArticleCreateDTO
from domain.entities.article.models import Article


class ArticleDTOToModelMapper:
    @staticmethod
    def from_create_dto(dto: ArticleCreateDTO) -> Article:
        return Article(
            author_id=dto.author_id,
            title=dto.title,
            body=dto.body,
            status=dto.status,
        )
