from pydantic_settings import BaseSettings
from pydantic import model_validator
from pathlib import Path

from setup.configs import BaseSettingsConfig, BASE_DIR


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


class PepperConfig(BaseSettingsConfig):
    pepper: str

    class Config:
        env_prefix = "PASSWORD_"


class CodeGeneratorConfig(BaseSettingsConfig):
    min_val: int
    max_val: int

    class Config:
        env_prefix = "CODE_GENERATOR_"
