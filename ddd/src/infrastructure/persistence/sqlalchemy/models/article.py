from enum import Enum
from functools import partial
from datetime import datetime, UTC

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from .base import mapper_registry
from domain.entities.article.models import Article

UTC_NOW = partial(datetime.now, UTC)


class ArticleStatus(Enum):
    draft = "df"
    published = "pb"


articles_table = sa.Table(
    "articles",
    mapper_registry.metadata,
    sa.Column(
        "id",
        sa.BigInteger,
        primary_key=True,
        unique=True,
    ),
    sa.Column(
        "title",
        sa.String(150),
    ),
    sa.Column(
        "body",
        sa.Text,
    ),
    sa.Column(
        "status",
        sa.String,
        default="draft",
    ),
    sa.Column(
        "created_at",
        sa.DateTime,
        server_default=sa.text("(now() at time zone 'utc')")
    ),
    sa.Column(
        "updated_at",
        sa.DateTime,
        default=None,
        onupdate=UTC_NOW
    ),
    sa.Column(
        "author_id",
        sa.BigInteger,
        sa.ForeignKey("users.id")
    ),
)

def map_articles_table() -> None:
    mapper_registry.map_imperatively(
        Article,
        articles_table,
        properties={
            "author": relationship(
                "User",
                back_populates="articles",
                cascade="all, delete-orphan",
            )
        }
    )
