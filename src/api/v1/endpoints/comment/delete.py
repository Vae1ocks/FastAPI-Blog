from dishka import FromDishka
from fastapi import Depends, status

from application.use_cases.comment.delete import CommentDeleteUseCase
from domain.entities.comment.models import CommentId
from .router import router
from dishka.integrations.fastapi import inject

from ...common.dependencies.jwt_bearer import http_bearer


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def comment_delete(
    comment_id: CommentId,
    delete_usecase: FromDishka[CommentDeleteUseCase],
    token=Depends(http_bearer),  # noqa, for api documentation
):
    await delete_usecase.execute(comment_id=comment_id)
