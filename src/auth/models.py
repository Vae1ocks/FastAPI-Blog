from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, validates

from src.models import Base


class User(Base):
    email: Mapped[str] = mapped_column(unique=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    password: Mapped[str]

    is_active: Mapped[bool] = mapped_column(default=True, server_default="true")
    is_confirmed: Mapped[bool] = mapped_column(default=False, server_default="false")
    is_superuser: Mapped[bool] = mapped_column(default=False, server_default="false")

    @validates("password")
    def validate_password(self, key, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
