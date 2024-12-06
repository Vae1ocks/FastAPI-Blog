from abc import ABC, abstractmethod
from typing import BinaryIO


class ImageChecker(ABC):
    @staticmethod
    @abstractmethod
    def check(file: BinaryIO) -> None:
        ...


class ImageLoader(ABC):
    @abstractmethod
    def __call__(self, image: BinaryIO):
        ...
