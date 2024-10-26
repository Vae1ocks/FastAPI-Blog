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
        default=UTC_NOW,
        server_default=text("(now() at time zone 'utc')"),
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        default=None, onupdate=UTC_NOW
    )

    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    author: Mapped["User"] = relationship(back_populates="articles")

    __table_args__ = (Index("article_title_index", "title"),)
