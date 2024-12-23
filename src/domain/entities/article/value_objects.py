from dataclasses import dataclass

from ..common.value_objects import BaseValueObject
from ..common.exceptions import ShortTitleLengthException, LongTitleLengthException


@dataclass(frozen=True)
class ArticleTitle(BaseValueObject):
    value: str | None = None

    def validate(self):
        if self.value is None:
            return
        if len(self.value) < 5:
            raise ShortTitleLengthException(5)
        if len(self.value) > 150:
            raise LongTitleLengthException(150)


@dataclass(frozen=True)
class ArticleBody(BaseValueObject):
    value: str | None = None

    def validate(self):
        pass
