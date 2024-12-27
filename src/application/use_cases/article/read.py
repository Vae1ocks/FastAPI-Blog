from dataclasses import dataclass

from application.dto.article.article_read import ArticleReadDTO, ArticleListDTO
from application.dto.common.list import ListObjectsDTO
from application.errors.common.not_found import DoesNotExist
from application.mappers.article.model_to_dto import ArticleModelToDTOMapper
from application.services.article.read import ArticleReadService
from domain.entities.article.models import ArticleId, Article


@dataclass
class ArticleListUseCase:
    read_service: ArticleReadService

    async def execute(self, dto: ListObjectsDTO) -> list[ArticleListDTO]:
        articles: list[Article | None] = await self.read_service.read_list(dto=dto)
        dtos: list[ArticleListDTO] = ArticleModelToDTOMapper.to_list_dtos(models=articles)
        return dtos
