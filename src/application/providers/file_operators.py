from abc import ABC, abstractmethod

from io import BytesIO

class ImageChecker(ABC):
    @staticmethod
    @abstractmethod
    def check(file: BytesIO):
        ...


class ImageLoader(ABC):
    @abstractmethod
    def __call__(self, image: BytesIO):
        ...
