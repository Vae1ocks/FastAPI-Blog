from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.models import Base


class User(Base):
    email: Mapped[str] = mapped_column(unique=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)

    is_active: Mapped[bool] = mapped_column(default=True, server_default="true")
    is_verified: Mapped[bool] = mapped_column(default=False, server_default="false")
    is_superuser: Mapped[bool] = mapped_column(default=False, server_default="false")
