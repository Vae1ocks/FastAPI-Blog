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


configs = AllConfigs()
