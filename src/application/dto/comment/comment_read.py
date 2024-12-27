from dataclasses import dataclass
from datetime import datetime

from domain.entities.comment.models import CommentId
from domain.entities.comment.value_objects import CommentBody
from ..user.user_read import UserListDTO


@dataclass(frozen=True, slots=True)
class CommentReadDTO:
    id: CommentId
    body: CommentBody
    author: UserListDTO
    created_at: datetime
    updated_at: datetime | None = None
