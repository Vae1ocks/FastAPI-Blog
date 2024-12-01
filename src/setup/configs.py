from pydantic_settings import BaseSettings
from pydantic import model_validator
from pathlib import Path

from infrastructure.celery.config import RedisConfig, SMTPConfig, CeleryConfig
from infrastructure.persistence.config import DatabaseConfig, SqlaEngineConfig, SqlaSessionConfig
from infrastructure.providers.config import FileConfig, PepperConfig, CodeGeneratorConfig

BASE_DIR = Path(__file__).parent.parent.parent.parent


class BaseSettingsConfig(BaseSettings):
    class Config:
        env_file = f"{BASE_DIR}/.env"
        extra = "ignore"


class SessionConfig(BaseSettingsConfig):
    secret: str

    class Config:
        env_prefix = "SESSION_"


class UvicornConfig(BaseSettingsConfig):
    host: str = "localhost"
    port: int = 8000
    reload: bool = True

    class Config:
        env_prefix = "UVICORN_"


class AllConfigs(BaseSettingsConfig):
    db: DatabaseConfig = DatabaseConfig()
    sqla_eng: SqlaEngineConfig = SqlaEngineConfig()
    sqla_sess: SqlaSessionConfig = SqlaSessionConfig()
    redis: RedisConfig = RedisConfig()
    smtp: SMTPConfig = SMTPConfig()
    file: FileConfig = FileConfig()
    pepper: PepperConfig = PepperConfig()
    code_generator: CodeGeneratorConfig = CodeGeneratorConfig()
    celery: CeleryConfig = CeleryConfig()
    session: SessionConfig = SessionConfig()
    uvicorn: UvicornConfig = UvicornConfig()


configs = AllConfigs()
