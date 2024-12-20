from enum import StrEnum
from pathlib import Path

from infrastructure.celery.config import RedisConfig, SMTPConfig, CeleryConfig
from infrastructure.persistence.config import DatabaseConfig, SqlaEngineConfig, SqlaSessionConfig
from infrastructure.processors.config import FileConfig, PepperConfig, CodeGeneratorConfig, JWTConfig
from setup.base_config import BaseSettingsConfig

BASE_DIR = Path(__file__).parent.parent.parent


class SessionConfig(BaseSettingsConfig):
    secret: str

    class Config:
        env_file = f"{BASE_DIR}/.env"
        env_prefix = "SESSION_"


class UvicornConfig(BaseSettingsConfig):
    host: str = "localhost"
    port: int = 8000
    reload: bool = True

    class Config:
        env_file = f"{BASE_DIR}/.env"
        env_prefix = "UVICORN_"


class LogLevelsEnum(StrEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LoggingConfig(BaseSettingsConfig):
    level: LogLevelsEnum

    class Config:
        env_file = f"{BASE_DIR}/.env"
        env_prefix = "LOGGING_"


class AllConfigs(BaseSettingsConfig):
    db: DatabaseConfig = DatabaseConfig()  # noqa
    sqla_eng: SqlaEngineConfig = SqlaEngineConfig()  # noqa
    sqla_sess: SqlaSessionConfig = SqlaSessionConfig()  # noqa
    redis: RedisConfig = RedisConfig()  # noqa
    smtp: SMTPConfig = SMTPConfig()  # noqa
    file: FileConfig = FileConfig()  # noqa
    pepper: PepperConfig = PepperConfig()  # noqa
    code_generator: CodeGeneratorConfig = CodeGeneratorConfig()  # noqa
    celery: CeleryConfig = CeleryConfig()  # noqa
    session: SessionConfig = SessionConfig()  # noqa
    uvicorn: UvicornConfig = UvicornConfig()  # noqa
    jwt: JWTConfig = JWTConfig()  # noqa
    logging: LoggingConfig = LoggingConfig()  # noqa


configs = AllConfigs()
