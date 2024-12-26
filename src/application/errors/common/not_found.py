from dataclasses import dataclass

from application.common.error import ApplicationError


@dataclass(eq=False)
class DoesNotExist(ApplicationError):
    obj_name: str
    obj_id: int

    @property
    def message(self) -> str:
        return f"The {self.obj_name.capitalize()} with id={self.obj_id} does not exist"

    def __str__(self) -> str:
        return self.message
