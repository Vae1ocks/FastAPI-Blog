from enum import Enum
from functools import partial
from datetime import datetime, UTC
from typing import TYPE_CHECKING

from sqlalchemy import String, Text, ForeignKey, Index, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base

if TYPE_CHECKING:
    from src.auth.models import User

UTC_NOW = partial(datetime.now, UTC)


class ArticleStatus(Enum):
    draft = "df"
    published = "pb"


class Article(Base):
    title: Mapped[str] = mapped_column(String(150))
    body: Mapped[str] = mapped_column(Text)
    status: Mapped[ArticleStatus] = mapped_column(default=ArticleStatus.draft)
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("(now() at time zone 'utc')"),
    )
    updated_at: Mapped[datetime | None] = mapped_column(default=None, onupdate=UTC_NOW)

    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    author: Mapped["User"] = relationship(back_populates="articles")
    comments: Mapped[list["Comment"]] = relationship(back_populates="article")

    __table_args__ = (Index("article_title_index", "title"),)


class Comment(Base):
    body: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("(now() at time zone 'utc')"),
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        default=None, server_default=None, onupdate=UTC_NOW
    )

    article_id: Mapped[int] = mapped_column(
        ForeignKey("articles.id", ondelete="CASCADE"),
    )
    article: Mapped["Article"] = relationship(back_populates="comments")

    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
    )
    author: Mapped["User"] = relationship(back_populates="comments")
