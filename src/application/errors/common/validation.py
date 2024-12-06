from dataclasses import dataclass

from application.common.error import ApplicationError


@dataclass
class ObjectNotExistsError(ApplicationError):
    obj: str
    id: int

    @property
    def message(self) -> str:
        return f"{self.obj.capitalize()} with {id=} does not exists"

    def __str__(self) -> str:
        return self.message


class FileNotImageError(ApplicationError):
    message = "File is not an image"

    def __str__(self) -> str:
        return self.message


@dataclass
class AlreadyExistsError(ApplicationError):
    obj: str
    id: int

    @property
    def message(self) -> str:
        return f"{self.obj.capitalize()} with {id=} already exists"

    def __str__(self) -> str:
        return self.message
