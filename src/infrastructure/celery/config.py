from pydantic import RedisDsn

from infrastructure.config import BaseSettingsConfig


class RedisSettings(BaseSettingsConfig):
    port: str
    host: str

    @property
    def url(self) -> RedisDsn:
        return f"redis://{self.host}:{self.port}"

    class Config:
        env_prefix = "REDIS_"


class SMTPSettings(BaseSettingsConfig):
    host: str
    host_user: str
    host_password: str
    port: int

    class Config:
        env_prefix = "SMTP_"


class CeleryConfig(BaseSettingsConfig):
    redis: RedisSettings = RedisSettings()
    smtp: SMTPSettings = SMTPSettings()


celery_settings = CeleryConfig()
