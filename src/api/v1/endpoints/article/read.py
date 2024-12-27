from dishka import FromDishka
from dishka.integrations.fastapi import inject

from application.dto.article.article_read import ArticleListDTO
from application.dto.common.list import ListObjectsDTO
from application.use_cases.article.read import ArticleListUseCase
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

