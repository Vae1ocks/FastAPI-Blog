import aiofiles
from pathlib import Path
from datetime import datetime, UTC
from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, validates, relationship

from src.models import Base
from src.config import settings

if TYPE_CHECKING:
    from src.articles.models import Article, Comment


class User(Base):
    email: Mapped[str] = mapped_column(unique=True)
    username: Mapped[str] = mapped_column(String(25), unique=True)
    password: Mapped[str]
    image_path: Mapped[str] = mapped_column(nullable=True)

    articles: Mapped[list["Article"]] = relationship(back_populates="author")
    comments: Mapped[list["Comment"]] = relationship(back_populates="author")

    is_active: Mapped[bool] = mapped_column(default=True, server_default="true")
    is_confirmed: Mapped[bool] = mapped_column(default=False, server_default="false")
    is_superuser: Mapped[bool] = mapped_column(default=False, server_default="false")

    @validates("password")
    def validate_password(self, key, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return value

    @validates("username")
    def validate_username(self, key, value):
        if len(value) < 3:
            raise ValueError("Username must be at least 3 characters long")
        elif len(value) > 25:
            raise ValueError("Username must be up to 25 characters")
        return value

    async def save_picture(
        self,
        file,
        directory=settings.files.users_profile_images_directory,
    ):
        path = Path(directory)
        file_extension = Path(file.filename).suffix
        timestamp = datetime.now(UTC).strftime(
            settings.files.file_save_time_pattern,
        )
        filepath = path / f"{self.username}-{timestamp}{file_extension}"

        async with aiofiles.open(filepath, "wb") as file_:
            contents = await file.read()
            await file_.write(contents)

        self.image_path = str(filepath)

    @property
    async def file(self):
        image_path = self.image_path
        if not image_path:
            return None

        path = Path(image_path)
        if path.exists():
            async with aiofiles.open(path) as file:
                return file.read()
        raise FileNotFoundError(f"file {image_path} not found")
