from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, RedisDsn, DirectoryPath, model_validator

from pathlib import Path

BASE_DIR = Path(__file__).parent.parent


class BaseSettingsConfig(BaseSettings):
    class Config:
        env_file = f"{BASE_DIR}/.env"
        extra = "ignore"


class FileConfig(BaseSettingsConfig):
    file_directory: str = f"{BASE_DIR}/files/"
    image_directory: str = f"{BASE_DIR}/files/images/"
    users_profile_images_directory: str = f"{BASE_DIR}/files/images/users/profiles"
    file_save_time_pattern: str = "%Y.%m.%d-%H:%M:%S"

    @model_validator(mode="after")
    def check_if_path_exists_or_create(self):
        for path_attr_name in (
            "file_directory",
            "image_directory",
            "users_profile_images_directory",
        ):
            path_ = getattr(self, path_attr_name)
            path = Path(path_)
            if path_ and not path.exists():
                path.mkdir(parents=True, exist_ok=True)
        return self


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
    algorithm: str = "HS256"
    access_token_lifespan_minutes: int = 5
    access_token_type: str = "str"
    refresh_token_lifespan_days: int = 15
    refresh_token_type: str = "refresh"

    class Config:
        env_prefix = "JWT_"


class SessionSettings(BaseSettingsConfig):
    secret: str

    class Config:
        env_prefix = "SESSION_"


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
    port: str

    class Config:
        env_prefix = "SMTP_"


class Settings(BaseSettings):
    db: DatabaseSettings = DatabaseSettings()
    jwt: JWTSettings = JWTSettings()
    session: SessionSettings = SessionSettings()
    redis: RedisSettings = RedisSettings()
    smtp: SMTPSettings = SMTPSettings()
    files: FileConfig = FileConfig()


settings = Settings()
