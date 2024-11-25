from abc import ABC, abstractmethod


class CodeIntGenerator(ABC):
    @abstractmethod
    def __call__(self):
        ...
