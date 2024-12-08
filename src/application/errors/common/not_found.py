from dataclasses import dataclass

from application.common.error import ApplicationError


@dataclass(eq=False)
class NotFoundError(ApplicationError):
    obj_name: str
    id: str

    @property
    def message(self) -> str:
        return f"The {self.obj_name.capitalize()} with {id=}"

    def __str__(self) -> str:
        return self.message
