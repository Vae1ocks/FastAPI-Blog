from pydantic_settings import BaseSettings
from pydantic import model_validator
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent.parent

class BaseSettingsConfig(BaseSettings):
    class Config:
        env_file = f"{BASE_DIR}/.env"
        extra = "ignore"


class FileConfig(BaseSettingsConfig):
    file_directory: str = f"{BASE_DIR}/files/"
    image_directory: str = f"{BASE_DIR}/files/images/"
    users_profile_images_directory: str = f"{BASE_DIR}/files/images/users/profiles"
    file_save_time_pattern: str = "%Y.%m.%d-%H:%M:%S.%f"

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


class Settings(BaseSettings):
    files: FileConfig = FileConfig()


settings = Settings()
