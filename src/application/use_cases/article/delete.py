import logging
from dataclasses import dataclass

from application.commiter import Commiter
from application.errors.common.no_permission import NoPermissionError
from application.services.article.delete import ArticleDeleteService
from domain.entities.article.models import ArticleId, Article
from domain.entities.user.models import UserId
from infrastructure.managers.jwt import JWTTokenManager

logger = logging.getLogger(__name__)


@dataclass
class ArticleDeleteUseCase:
    delete_service: ArticleDeleteService
    commiter: Commiter
    jwt_token_manager: JWTTokenManager

    async def execute(self, article_id: ArticleId) -> None:
        logger.debug("Executing ArticleDeleteUseCase: started")
        user_id: UserId = self.jwt_token_manager.get_subject_id_from_request_token()
        article: Article = await self.delete_service(article_id=article_id)
        if article.author_id != user_id:
            logger.debug(
                "Executing ArticleDeleteUseCase: finished with NoPermissionError"
            )
            raise NoPermissionError()
        await self.commiter.commit()
        logger.debug("Executing ArticleDeleteUseCase: finished with commit")
