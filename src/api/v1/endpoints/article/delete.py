from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import Depends, status

from application.use_cases.article.delete import ArticleDeleteUseCase
from domain.entities.article.models import ArticleId
from .router import router
from ...common.dependencies.jwt_bearer import http_bearer


@router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def article_delete(
    article_id: ArticleId,
    delete_usecase: FromDishka[ArticleDeleteUseCase],
    token=Depends(http_bearer),  # noqa, for api documentation
):
    await delete_usecase.execute(article_id=article_id)
