from pydantic import BaseModel, model_validator

from domain.entities.article.models import ArticleStatus, ArticleId


class ArticleUpdateScheme(BaseModel):
    id: ArticleId
    title: str | None = None
    body: str | None = None
    status: ArticleStatus | None = None

    @model_validator(mode="after")
    def validate_values_not_none(self):
        if not self.title and not self.body and not self.status:
            raise ValueError(
                "You should provide title, body, or status"
            )
        return self
