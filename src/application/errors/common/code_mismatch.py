from dataclasses import dataclass

from application.common.error import ApplicationError


@dataclass
class CodeMismatchError(ApplicationError):
    message: str = "Code mismatch"

    def __str__(self) -> str:
        return self.message
