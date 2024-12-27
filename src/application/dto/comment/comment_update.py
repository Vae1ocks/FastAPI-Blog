from dataclasses import dataclass

from domain.entities.comment.models import CommentId
from domain.entities.comment.value_objects import CommentBody


@dataclass(frozen=True, slots=True)
class CommentUpdateDTO:
    id: CommentId
    body: CommentBody
