from datetime import datetime

from pydantic import BaseModel

from api.v1.schemes.comment.read import CommentReadScheme
from api.v1.schemes.user.user_read import UserListScheme


class ArticleReadScheme(BaseModel):
    id: int
    title: str
    body: str
    status: str
    created_at: datetime
    updated_at: datetime
    author: UserListScheme
    comments: list[CommentReadScheme]
