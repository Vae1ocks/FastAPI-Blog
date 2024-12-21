from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import Depends

from application.dto.article.article_create import ArticleCreateDTO
from application.dto.article.article_read import ArticleReadDTO
from application.use_cases.article.create import ArticleCreateUseCase
from .router import router
from ...common.dependencies.jwt_bearer import http_bearer
from ...mappers.article.dto_to_scheme import ArticleDTOToSchemeMapper
from ...mappers.article.scheme_to_dto import ArticleSchemeToDTOMapper
from ...schemes.article.create import ArticleCreateScheme


@router.post("/create")
@inject
async def article_create(
    data: ArticleCreateScheme,
    create_usecase: FromDishka[ArticleCreateUseCase],
    token = Depends(http_bearer),
):
    dto: ArticleCreateDTO = ArticleSchemeToDTOMapper.to_create_dto(scheme=data)
    article_read: ArticleReadDTO = await create_usecase.execute(dto=dto)
    return ArticleDTOToSchemeMapper.to_read_scheme(dto=article_read)
