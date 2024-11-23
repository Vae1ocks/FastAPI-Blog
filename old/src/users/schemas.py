from datetime import datetime

from old.src.auth.schemas import BaseUser
from old.src.articles.schemas import ArticleList


class UserRead(BaseUser):
    articles: list[ArticleList]
    created_at: datetime

    class Config:
        from_attributes = True
