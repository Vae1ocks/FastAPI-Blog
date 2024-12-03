from functools import partial
from datetime import datetime, UTC

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from .base import mapper_registry
from domain.entities.comment.models import Comment

UTC_NOW = partial(datetime.now, UTC)


comments_table = sa.Table(
    "comments",
    mapper_registry.metadata,
    sa.Column(
        "id",
        sa.BigInteger,
        primary_key=True,
        unique=True,
    ),
    sa.Column(
        "body",
        sa.Text,
    ),
    sa.Column(
        "created_at",
        sa.DateTime,
        server_default=sa.text("(now() at time zone 'utc')"),
    ),
    sa.Column(
        "updated_at",
        sa.DateTime,
        default=None,
        onupdate=UTC_NOW,
    ),
    sa.Column(
        "article_id",
        sa.BigInteger,
        sa.ForeignKey("articles.id"),
    ),
    sa.Column(
        "author_id",
        sa.BigInteger,
        sa.ForeignKey("users.id"),
    ),
)


def map_comments_table() -> None:
    mapper_registry.map_imperatively(
        Comment,
        comments_table,
        properties={
            "article": relationship(
                "Article",
                back_populates="comments",
            ),
            "author": relationship(
                "User",
                back_populates="comments",
            )
        }
    )
