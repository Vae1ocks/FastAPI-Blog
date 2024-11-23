from dataclasses import dataclass

from domain.entities.comment.value_objects import CommentBody


@dataclass(frozen=True, slots=True)
class CommentUpdateDTO:
    id: str
    body: CommentBody
