from datetime import datetime

from pydantic import BaseModel

from src.auth.schemas import BaseUser
from src.articles.schemas import ArticleList


class UserRead(BaseUser):
    articles: list[ArticleList]
    created_at: datetime

    class Config:
        from_attributes = True
