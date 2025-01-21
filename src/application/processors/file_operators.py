from abc import ABC, abstractmethod
from typing import BinaryIO

from application.dto.other.file import FileDTO


class ImageChecker(ABC):
    @staticmethod
    @abstractmethod
    def check(file: BinaryIO) -> None:
        ...


class ImageLoader(ABC):
    @abstractmethod
    def __call__(self, image: FileDTO):
        ...
