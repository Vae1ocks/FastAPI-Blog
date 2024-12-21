from enum import Enum
from functools import partial
from datetime import datetime, UTC

import sqlalchemy as sa
from sqlalchemy.orm import relationship, composite

from domain.entities.article.value_objects import ArticleTitle, ArticleBody
from .base import mapper_registry
from domain.entities.article.models import Article, ArticleStatus

UTC_NOW = partial(datetime.now, UTC)


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
        "article_title",
        sa.String(150),
    ),
    sa.Column(
        "article_body",
        sa.Text,
    ),
    sa.Column(
        "article_status",
        sa.Enum(ArticleStatus),
        default=ArticleStatus.draft,
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
            ),
            "comments": relationship(
                "Comment",
                back_populates="article",
                cascade="all, delete-orphan",
            ),
            "title": composite(ArticleTitle, articles_table.c.article_title),
            "body": composite(ArticleBody, articles_table.c.article_body),
            "status": composite(ArticleStatus, articles_table.c.article_status),
        }
    )
