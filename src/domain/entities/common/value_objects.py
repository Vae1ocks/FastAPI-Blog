from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass(frozen=True)
class BaseValueObject(ABC):
    def __post_init__(self):
        self.validate()

    @abstractmethod
    def validate(self):
        pass
