from pathlib import Path

from pydantic import RedisDsn

from setup.base_config import BaseSettingsConfig

BASE_DIR = Path(__file__).parent.parent.parent.parent


class RedisConfig(BaseSettingsConfig):
    port: str
    host: str

    @property
    def url(self) -> RedisDsn:
        return f"redis://{self.host}:{self.port}"

    class Config:
        env_file = f"{BASE_DIR}/.env"
        env_prefix = "REDIS_"


class SMTPConfig(BaseSettingsConfig):
    host: str
    host_user: str
    host_password: str
    port: int

    class Config:
        env_file = f"{BASE_DIR}/.env"
        env_prefix = "SMTP_"


class CeleryConfig(BaseSettingsConfig):
    redis: RedisConfig = RedisConfig()
    smtp: SMTPConfig = SMTPConfig()


celery_config = CeleryConfig()
