from dishka import FromDishka
from dishka.integrations.fastapi import inject

from application.dto.article.article_read import ArticleListDTO, ArticleReadDTO
from application.dto.common.list import ListObjectsDTO
from application.use_cases.article.read import (
    ArticleListUseCase,
    ArticleReadDetailUseCase,
)
from domain.entities.article.models import ArticleId
from .router import router
from ...mappers.article.dto_to_scheme import ArticleDTOToSchemeMapper
from ...mappers.common.list_objects_mapper import ListObjectsOrderMapper


@router.get("")
@inject
async def list_articles(
    offset: int,
    limit: int,
    list_usecase: FromDishka[ArticleListUseCase],
    order: str | None = None,
):
    list_dto: ListObjectsDTO = ListObjectsOrderMapper.to_dto(
        offset=offset,
        limit=limit,
        order=order,
    )
    list_dtos: list[ArticleListDTO] = await list_usecase.execute(dto=list_dto)
    return ArticleDTOToSchemeMapper.to_list_scheme(dtos=list_dtos)


@router.get("/{article_id}")
@inject
async def article_read(
    article_id: ArticleId,
    detail_usecase: FromDishka[ArticleReadDetailUseCase],
):
    read_dto: ArticleReadDTO = await detail_usecase.execute(article_id=article_id)
    return ArticleDTOToSchemeMapper.to_read_scheme(dto=read_dto)
