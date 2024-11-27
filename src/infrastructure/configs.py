from pydantic_settings import BaseSettings
from pydantic import model_validator
from pathlib import Path

from infrastructure.celery.config import RedisConfig, SMTPConfig, CeleryConfig
from infrastructure.persistence.config import DatabaseConfig
from infrastructure.providers.config import FileConfig

BASE_DIR = Path(__file__).parent.parent.parent.parent


class BaseSettingsConfig(BaseSettings):
    class Config:
        env_file = f"{BASE_DIR}/.env"
        extra = "ignore"


class AllConfigs(BaseSettingsConfig):
    db: DatabaseConfig = DatabaseConfig()
    redis: RedisConfig = RedisConfig()
    smtp: SMTPConfig = SMTPConfig()
    file: FileConfig = FileConfig()
    celery: CeleryConfig = CeleryConfig()