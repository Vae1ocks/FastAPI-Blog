from dataclasses import dataclass

import logging

from application.commiter import Commiter
from application.dto.article.article_read import ArticleReadDTO
from application.dto.article.article_update import ArticleUpdateDTO
from application.errors.common.no_permission import NoPermissionError
from application.mappers.article.model_to_dto import ArticleModelToDTOMapper
from application.services.article.update import ArticleUpdateService
from domain.entities.article.models import Article
from domain.entities.user.models import UserId
from infrastructure.managers.jwt import JWTTokenManager

logger = logging.getLogger(__name__)


@dataclass
class ArticleUpdateUseCase:
    update_service: ArticleUpdateService
    jwt_token_manager: JWTTokenManager
    commiter: Commiter

    async def execute(self, dto: ArticleUpdateDTO) -> ArticleReadDTO:
        logger.debug("Executing ArticleUpdateUseCase: started")
        user_id: UserId = self.jwt_token_manager.get_subject_id_from_request_token()
        article: Article = await self.update_service(dto=dto)
        if article.author_id != user_id:
            logger.debug("Executing ArticleUpdateUseCase: finished with NoPermissionError")
            raise NoPermissionError()
        await self.commiter.commit()
        logger.debug("Executing ArticleUpdateUseCase: finished with commiting")
        return ArticleModelToDTOMapper.to_read_dto(model=article)
