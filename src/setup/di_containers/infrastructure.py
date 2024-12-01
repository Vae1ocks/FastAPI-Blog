from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton, Factory

from infrastructure.providers.code_generator import RandomIntegerCodeGenerator
from infrastructure.providers.file_operators import (
    ImageCheckerImpl,
    FileSystemImageLoader,
)
from infrastructure.providers.password_hasher_bcrypt import BcryptPasswordHasher
from setup.configs import configs


class InfrastructureContainer(DeclarativeContainer):
    password_hasher: BcryptPasswordHasher = Factory(
        BcryptPasswordHasher,
        pepper=configs.pepper.pepper,
    )

    image_checker: ImageCheckerImpl = Singleton(ImageCheckerImpl)
    image_loader: FileSystemImageLoader = Factory(
        FileSystemImageLoader,
        directory=configs.file.users_profile_images_directory,
        file_name_patter=configs.file.file_save_time_pattern,
    )

    code_generator: RandomIntegerCodeGenerator = Singleton(
        RandomIntegerCodeGenerator,
        min_val=configs.code_generator.min_val,
        max_val=configs.code_generator.max_val,
    )
