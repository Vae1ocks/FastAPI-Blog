import sqlalchemy as sa
from sqlalchemy.orm import relationship

from .base import mapper_registry
from domain.entities.user.models import User


users_table = sa.Table(
    "users",
    mapper_registry.metadata,
    sa.Column(
        "id",
        sa.BigInteger,
        primary_key=True,
        unique=True,
    ),
    sa.Column(
        "email",
        sa.String,
    ),
    sa.Column(
        "username",
        sa.String(25),
    ),
    sa.Column(
        "password",
        sa.String,
    ),
    sa.Column(
        "image_path",
        sa.String,
    ),
    sa.Column(
        "created_at",
        sa.DateTime,
        server_default=sa.text("(now() at time zone 'utc')"),
    ),
    sa.Column("is_active", sa.Boolean, server_default=sa.false()),
    sa.Column(
        "is_confirmed",
        sa.Boolean,
        server_default=sa.false(),
    ),
    sa.Column(
        "is_superuser",
        sa.Boolean,
        server_default=sa.false(),
    ),
)


def map_users_table() -> None:
    mapper_registry.map_imperatively(
        User,
        users_table,
        properties={
            "articles": relationship(
                "Article",
                back_populates="author",
            ),
            "comments": relationship(
                "Comment",
                back_populates="author",
            ),
        },
    )
