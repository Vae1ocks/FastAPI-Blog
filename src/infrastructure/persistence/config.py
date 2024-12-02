from pydantic import PostgresDsn
from pathlib import Path

from setup.base_config import BaseSettingsConfig

BASE_DIR = Path(__file__).parent.parent.parent.parent


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
        env_file = f"{BASE_DIR}/.env"
        env_prefix = "DB_"


class SqlaEngineConfig(BaseSettingsConfig):
    echo: bool
    echo_pool: bool
    pool_size: int
    max_overflow: int

    class Config:
        env_file = f"{BASE_DIR}/.env"
        env_prefix = "SQLA_ENG_"


class SqlaSessionConfig(BaseSettingsConfig):
    autoflush: bool
    autocommit: bool
    expire_on_commit: bool

    class Config:
        env_file = f"{BASE_DIR}/.env"
        env_prefix = "SQLA_SESS_"


db_config: DatabaseConfig = DatabaseConfig()
