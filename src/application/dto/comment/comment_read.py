from dataclasses import dataclass
from datetime import datetime

from ..user.user_read import UserListDTO


@dataclass(frozen=True, slots=True)
class CommentReadDTO:
    id: int
    body: str
    author: UserListDTO
    created_at: datetime
    updated_at: datetime | None = None
