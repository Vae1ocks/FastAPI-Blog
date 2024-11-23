from dataclasses import dataclass

from ..common.value_objects import BaseValueObject
from ..common.exceptions import ShortTitleLengthException, LongTitleLengthException


@dataclass(frozen=True)
class ArticleTitle(BaseValueObject):
    title: str

    def validate(self):
        if len(self.title) < 5:
            raise ShortTitleLengthException(5)
        if len(self.title) > 150:
            raise LongTitleLengthException(150)


@dataclass(frozen=True)
class ArticleBody:
    text: str
