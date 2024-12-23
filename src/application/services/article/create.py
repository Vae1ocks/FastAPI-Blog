import logging
from dataclasses import dataclass

from application.commiter import Commiter
from application.dto.article.article_create import ArticleCreateDTO
from domain.entities.article.models import Article
from domain.exceptions.base import DomainFieldError
from domain.repositories.article_repository import ArticleRepository

logger = logging.getLogger(__name__)


@dataclass
class ArticleCreateService:
    article_repository: ArticleRepository
    commiter: Commiter

    async def create(self, dto: ArticleCreateDTO) -> Article:
        if dto.author_id is None:
            logger.error("ArticleDTO.author_id is None")
            raise DomainFieldError()
        article = Article(
            author_id=dto.author_id,
            title=dto.title,
            body=dto.body,
            status=dto.status,
        )
        self.article_repository.add(article)
        await self.commiter.commit()
        article: Article = await self.article_repository.get_by_id(article.id)
        return article
