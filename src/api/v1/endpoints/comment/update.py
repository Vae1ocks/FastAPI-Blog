from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import Depends

from api.v1.common.dependencies.jwt_bearer import http_bearer
from api.v1.endpoints.comment.router import router
from api.v1.mappers.comment.dto_to_scheme import CommentDTOToSchemeMapper
from api.v1.mappers.comment.scheme_to_dto import CommentSchemeToDTOMapper
from api.v1.schemes.comment.update import CommentUpdateScheme
from application.dto.comment.comment_read import CommentReadDTO
from application.dto.comment.comment_update import CommentUpdateDTO
from application.use_cases.comment.update import CommentUpdateUseCase
from domain.entities.comment.models import CommentId


@router.patch("/{comment_id}")
@inject
async def comment_update_partial(
    comment_id: CommentId,
    data: CommentUpdateScheme,
    update_usecase: FromDishka[CommentUpdateUseCase],
    token=Depends(http_bearer),  # noqa, for api documentation
):
    update_dto: CommentUpdateDTO = CommentSchemeToDTOMapper.to_update_dto(
        scheme=data, comment_id=comment_id
    )
    read_dto: CommentReadDTO = await update_usecase.execute(dto=update_dto)
    return CommentDTOToSchemeMapper.to_read_scheme(dto=read_dto)
