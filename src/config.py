from pydantic_settings import BaseSettings
from pydantic import PostgresDsn

from pathlib import Path

BASE_DIR = Path(__file__).parent.parent


class BaseSettingsConfig(BaseSettings):
    class Config:
        env_file = f"{BASE_DIR}/.env"


class DatabaseSettings(BaseSettingsConfig):
    @property
    def url(self) -> PostgresDsn:
        return (
            f"postgresql+asyncpg://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    echo: bool = False

    host: str
    port: str
    name: str
    user: str
    password: str


class Settings(BaseSettings):
    db: DatabaseSettings = DatabaseSettings()


settings = Settings()
