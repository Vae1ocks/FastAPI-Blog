from fastapi import APIRouter, Depends

from old.src.database import database
from old.src.auth.dependencies import get_current_active_user
from .schemas import ArticleCreate, ArticleList
from .utils import create_article
from .models import Article

router = APIRouter(
    prefix="/articles",
    tags=["Articles", "Comments"],
)


@router.post("/create")
async def create_user_article(
    data: ArticleCreate,
    user=Depends(
        get_current_active_user,
    ),
    session=Depends(
        database.session_dependency,
    ),
):
    article: Article = await create_article(
        user=user,
        data=data.model_dump(),
        session=session,
    )
    return ArticleList.model_validate(article, from_attributes=True)
