from pathlib import Path

from pydantic_settings import BaseSettings


class BaseSettingsConfig(BaseSettings):
    class Config:
        extra = "ignore"
