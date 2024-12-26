from dataclasses import dataclass

from application.common.error import ApplicationError


class FileNotImageError(ApplicationError):
    message = "File is not an image"

    def __str__(self) -> str:
        return self.message


@dataclass
class AlreadyExistsError(ApplicationError):
    obj_name: str
    id: int

    @property
    def message(self) -> str:
        return f"{self.obj_name.capitalize()} with {id=} already exists"

    def __str__(self) -> str:
        return self.message
