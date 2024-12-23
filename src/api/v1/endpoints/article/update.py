from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import Depends

from application.dto.article.article_read import ArticleReadDTO
from application.dto.article.article_update import ArticleUpdateDTO
from application.use_cases.article.update import ArticleUpdateUseCase
from .router import router
from ...common.dependencies.jwt_bearer import http_bearer
from ...mappers.article.dto_to_scheme import ArticleDTOToSchemeMapper
from ...mappers.article.scheme_to_dto import ArticleSchemeToDTOMapper
from ...schemes.article.update import ArticleUpdateScheme


@router.patch("{article_id}")
@inject
async def article_update_partial(
    data: ArticleUpdateScheme,
    update_usecase: FromDishka[ArticleUpdateUseCase],
    token=Depends(http_bearer),  # noqa, for api documentation
):
    dto: ArticleUpdateDTO = ArticleSchemeToDTOMapper.to_update_dto(scheme=data)
    article_read: ArticleReadDTO = await update_usecase.execute(dto=dto)
    return ArticleDTOToSchemeMapper.to_read_scheme(dto=article_read)
