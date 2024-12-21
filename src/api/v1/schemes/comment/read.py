from datetime import datetime

from pydantic import BaseModel

from api.v1.schemes.user.user_read import UserReadScheme


class CommentReadScheme(BaseModel):
    id: int
    body: str
    author: UserReadScheme
    created_at: datetime
    updated_at: datetime | None = None
