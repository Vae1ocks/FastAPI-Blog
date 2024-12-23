from dataclasses import dataclass

from application.common.error import ApplicationError


@dataclass(eq=False)
class NoPermissionError(ApplicationError):
    message: str = "You haven't permission to do this"

    def __str__(self) -> str:
        return self.message
