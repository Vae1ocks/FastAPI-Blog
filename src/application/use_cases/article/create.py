import logging
from dataclasses import dataclass

from application.dto.article.article_create import ArticleCreateDTO
from application.dto.article.article_read import ArticleReadDTO
from application.mappers.article.model_to_dto import ArticleModelToDTOMapper
from application.services.article.create import ArticleService
from domain.entities.article.models import Article
from domain.entities.user.models import UserId
from infrastructure.managers.jwt import JWTTokenManager

logger = logging.getLogger(__name__)


@dataclass
class ArticleCreateUseCase:
    article_service: ArticleService
    jwt_token_manager: JWTTokenManager

    async def execute(self, dto: ArticleCreateDTO) -> ArticleReadDTO:
        logger.debug("Executing ArticleCreateUseCase: started")
        user_id: UserId = self.jwt_token_manager.get_subject_id_from_request_token()
        total_dto: ArticleCreateDTO = ArticleCreateDTO(
            author_id=user_id,
            title=dto.title,
            body=dto.body,
            status=dto.status,
        )
        article: Article = await self.article_service.create(dto=total_dto)
        logger.debug("Executing ArticleCreateUseCase: finished")
        return ArticleModelToDTOMapper.to_read_dto(model=article)
