from dataclasses import dataclass

from application.dto.article.article_read import ArticleReadDTO, ArticleListDTO
from application.dto.common.list import ListObjectsDTO
from application.mappers.article.model_to_dto import ArticleModelToDTOMapper
from application.services.article.read import ArticleReadService
from domain.entities.article.models import ArticleId, Article


@dataclass
class ArticleReadDetailUseCase:
    read_service: ArticleReadService

    async def execute(self, article_id: ArticleId) -> ArticleReadDTO:
        article: Article = await self.read_service.read_by_id(article_id)
        dto: ArticleReadDTO = ArticleModelToDTOMapper.to_read_dto(model=article)
        return dto


@dataclass
class ArticleListUseCase:
    read_service: ArticleReadService

    async def execute(self, dto: ListObjectsDTO) -> list[ArticleListDTO]:
        articles: list[Article | None] = await self.read_service.read_list(dto=dto)
        dtos: list[ArticleListDTO] = ArticleModelToDTOMapper.to_list_dtos(models=articles)
        return dtos
