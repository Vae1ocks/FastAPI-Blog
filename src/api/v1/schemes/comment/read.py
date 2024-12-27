from datetime import datetime

from pydantic import BaseModel

from api.v1.schemes.user.user_read import UserListScheme
from domain.entities.comment.models import CommentId


class CommentReadScheme(BaseModel):
    id: CommentId
    body: str
    author: UserListScheme
    created_at: datetime
    updated_at: datetime | None = None
