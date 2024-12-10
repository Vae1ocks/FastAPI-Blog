from abc import ABC, abstractmethod


class PasswordHasher(ABC):
    @abstractmethod
    def hash(self, raw_password) -> bytes:
        ...

    @staticmethod
    @abstractmethod
    def add_pepper(raw_password: str, pepper: str) -> bytes:
        ...

    @abstractmethod
    def verify(self, raw_password: str, hashed_password: str) -> bool:
        ...