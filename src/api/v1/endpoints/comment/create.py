from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import Depends

from api.v1.common.dependencies.jwt_bearer import http_bearer
from api.v1.endpoints.comment.router import router
from api.v1.mappers.comment.dto_to_scheme import CommentDTOToSchemeMapper
from api.v1.mappers.comment.scheme_to_dto import CommentSchemeToDTOMapper
from api.v1.schemes.comment.create import CommentCreateScheme
from application.dto.comment.comment_create import CommentCreateDTO
from application.dto.comment.comment_read import CommentReadDTO
from application.use_cases.comment.create import CommentCreateUseCase
from domain.entities.article.models import ArticleId


@router.post("/{article_id}")
@inject
async def comment_create(
    article_id: ArticleId,
    data: CommentCreateScheme,
    create_usecase: FromDishka[CommentCreateUseCase],
    token=Depends(http_bearer),  # noqa, for api documentation
):
    create_dto: CommentCreateDTO = CommentSchemeToDTOMapper.to_create_dto(
        scheme=data, article_id=article_id
    )
    read_dto: CommentReadDTO = await create_usecase.execute(dto=create_dto)
    return CommentDTOToSchemeMapper.to_read_scheme(dto=read_dto)
