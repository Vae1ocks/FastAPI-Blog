from pydantic import BaseModel


class CommentCreateScheme(BaseModel):
    body: str