from pydantic_settings import BaseSettings
from pydantic import PostgresDsn

from pathlib import Path

BASE_DIR = Path(__file__).parent.parent


class BaseSettingsConfig(BaseSettings):
    class Config:
        env_file = f"{BASE_DIR}/.env"
        extra = "ignore"


class DatabaseSettings(BaseSettingsConfig):
    @property
    def url(self) -> PostgresDsn:
        return (
            f"postgresql+asyncpg://{self.user}:{self.password}"
            f"@{self.host}:{self.port}/{self.name}"
        )

    echo: bool = False

    host: str
    port: str
    name: str
    user: str
    password: str

    class Config:
        env_prefix = "DB_"


class JWTSettings(BaseSettingsConfig):
    secret: str
    algorithm: str = 'HS256'
    access_token_expire_minutes: int = 5

    class Config:
        env_prefix = "JWT_"


class SessionSettings(BaseSettingsConfig):
    secret: str

    class Config:
        env_prefix = "SESSION_"


class Settings(BaseSettings):
    db: DatabaseSettings = DatabaseSettings()
    jwt: JWTSettings = JWTSettings()
    session: SessionSettings = SessionSettings()

settings = Settings()
