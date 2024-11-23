from dataclasses import dataclass

from domain.entities.comment.value_objects import CommentBody


@dataclass(frozen=True, slots=True)
class CommentCreateDTO:
    user_id: int
    article_id: int
    body: CommentBody
