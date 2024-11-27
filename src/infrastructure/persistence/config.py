from pydantic import PostgresDsn
from pydantic_settings import BaseSettings

from setup.configs import BaseSettingsConfig


class DatabaseConfig(BaseSettingsConfig):
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


class DbConfig(BaseSettings):
    db: DatabaseConfig = DatabaseConfig()


db_config: DbConfig = DbConfig()
