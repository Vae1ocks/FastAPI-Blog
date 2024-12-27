from pydantic import BaseModel


class CommentUpdateScheme(BaseModel):
    body: str
