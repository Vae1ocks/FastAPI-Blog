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


class SqlaConfig(BaseSettings):
    echo: bool
    echo_pool: bool
    pool_size: int
    max_overflow: int

    class Config:
        env_prefix = "SQLA_"


db_config: DatabaseConfig = DatabaseConfig()
