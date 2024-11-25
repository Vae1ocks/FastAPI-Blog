from abc import ABC, abstractmethod

from io import BytesIO

class ImageChecker(ABC):
    @abstractmethod
    def __call__(self, file: BytesIO):
        ...


class ImageLoader(ABC):
    @abstractmethod
    def __call__(self, image: BytesIO):
        ...
