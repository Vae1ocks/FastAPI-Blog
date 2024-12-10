from abc import ABC, abstractmethod


class RandomCodeGenerator(ABC):
    @abstractmethod
    def __call__(self):
        ...
