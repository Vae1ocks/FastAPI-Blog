from dataclasses import dataclass

from application.dto.comment.comment_update import CommentUpdateDTO
from application.errors.common.not_found import DoesNotExist
from domain.entities.comment.models import Comment
from domain.entities.common.value_objects import BaseValueObject
from domain.repositories.comment_repository import CommentRepository


@dataclass
class CommentUpdateService:
    comment_repository: CommentRepository

    async def __call__(self, dto: CommentUpdateDTO) -> Comment:
        comment: Comment | None = await self.comment_repository.get_by_id(
            comment_id=dto.id
        )
        if comment is None:
            raise DoesNotExist(obj_name="Comment", obj_id=dto.id)

        for slot in dto.__slots__:  # noqa
            if slot == "id":
                continue
            attr = getattr(dto, slot)

            if attr is None:
                continue

            elif isinstance(attr, BaseValueObject):
                if attr.value is None:
                    continue

            setattr(comment, slot, attr)
        self.comment_repository.add(comment)
        return comment
