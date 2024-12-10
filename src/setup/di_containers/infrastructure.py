from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton, Factory

from infrastructure.processors.code_generator import RandomIntegerCodeGenerator
from infrastructure.processors.email_sender import EmailSender
from infrastructure.processors.file_operators import (
    ImageCheckerImpl,
    FileSystemImageLoader,
)
from infrastructure.processors.jwt_processor import (
    JWTGeneralTokenProcessor,
    JWTAccessTokenProcessor,
    JWTRefreshTokenProcessor,
    JWTTokenProcessor,
)
from infrastructure.processors.password_hasher_bcrypt import BcryptPasswordHasher
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
    email_sender: EmailSender = Singleton(
        EmailSender,
        host=configs.smtp.host,
        host_user=configs.smtp.host_user,
        host_password=configs.smtp.host_password,
        port=configs.smtp.port,
    )

    jwt_general_processor: JWTGeneralTokenProcessor = Singleton(
        JWTGeneralTokenProcessor,
        secret=configs.jwt.secret,
        algorithm=configs.jwt.algorithm,
    )
    jwt_access_processor: JWTAccessTokenProcessor = Singleton(
        JWTAccessTokenProcessor,
        expire_minutes=configs.jwt.access_expire_minutes,
        token_type=configs.jwt.access_token_type,
        jwt_general=jwt_general_processor,
    )
    jwt_refresh_processor: JWTRefreshTokenProcessor = Singleton(
        JWTRefreshTokenProcessor,
        expire_days=configs.jwt.refresh_expire_days,
        token_type=configs.jwt.refresh_token_type,
        jwt_general=jwt_general_processor,
    )
    jwt_processor: JWTTokenProcessor = Singleton(
        JWTTokenProcessor,
        access_token_processor=jwt_access_processor,
        refresh_token_processor=jwt_refresh_processor,
    )
