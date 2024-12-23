from dataclasses import dataclass

from ..common.exceptions import LongTitleLengthException
from ..common.value_objects import BaseValueObject


@dataclass(frozen=True)
class CommentBody(BaseValueObject):
    value: str

    def validate(self):
        if len(self.value) > 450:
            raise LongTitleLengthException(450)
