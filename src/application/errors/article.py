from dataclasses import dataclass

from application.common.error import ApplicationError


@dataclass
class ArticleTitleNotFound(ApplicationError):
    title: str

    @property
    def message(self) -> str:
        return f"Article not found by {self.title=}"

    def __str__(self) -> str:
        return self.message