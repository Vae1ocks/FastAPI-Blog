from dishka import Provider, provide

from application.processors.code_generator import RandomCodeGenerator
from application.processors.email_sender import MailSender
from application.processors.file_operators import ImageChecker, ImageLoader
from application.processors.password_hasher import PasswordHasher
from infrastructure.processors.code_generator import RandomIntegerCodeGenerator
from infrastructure.processors.email_sender import EmailSender
from infrastructure.processors.file_operators import (
    ImageCheckerImpl,
    FileSystemImageLoader,
)
from infrastructure.processors.jwt_processor import (
    JWTGeneralTokenProcessor,
    JWTAccessTokenProcessor,
    JWTRefreshTokenProcessor, JWTTokenProcessor,
)
from infrastructure.processors.password_hasher_bcrypt import BcryptPasswordHasher
from infrastructure.types import PasswordPepper, JWTAlgorithm, JWTSecret
from setup.configs import AllConfigs


class InfrastructureProvider(Provider):
    def __init__(self, configs: AllConfigs):
        super().__init__()
        self.configs = configs

    @provide
    def provide_password_pepper(self) -> PasswordPepper:
        return PasswordPepper(self.configs.pepper_settings.pepper)

    password_hasher = provide(
        source=BcryptPasswordHasher,
        provides=PasswordHasher,
    )

    image_checker = provide(
        source=ImageCheckerImpl,
        provides=ImageChecker,
    )

    @provide(provides=ImageLoader)
    def provide_image_loader(self) -> FileSystemImageLoader:
        return FileSystemImageLoader(
            directory=self.configs.file.users_profile_images_directory,
            file_name_patter=self.configs.file.file_save_time_pattern,
        )

    @provide(provides=RandomCodeGenerator)
    def provide_code_generator(self) -> RandomIntegerCodeGenerator:
        return RandomIntegerCodeGenerator(
            min_val=self.configs.code_generator.min_val,
            max_val=self.configs.code_generator.max_val,
        )

    @provide(provides=MailSender)
    def provide_email_sender(self) -> EmailSender:
        return EmailSender(
            host=self.configs.smtp.host,
            host_user=self.configs.smtp.host_user,
            host_password=self.configs.smtp.host_password,
            port=self.configs.smtp.port,
        )

    @provide
    def provide_jwt_general_processor(self) -> JWTGeneralTokenProcessor:
        return JWTGeneralTokenProcessor(
            secret=JWTSecret(self.configs.jwt.secret),
            algorithm=JWTAlgorithm(self.configs.jwt.algorithm),
        )

    @provide
    def provide_jwt_access_processor(
        self, jwt_general: JWTGeneralTokenProcessor
    ) -> JWTAccessTokenProcessor:
        return JWTAccessTokenProcessor(
            expire_minutes=self.configs.jwt.access_expire_minutes,
            token_type=self.configs.jwt.access_token_type,
            jwt_general=jwt_general,
        )

    @provide
    def provide_jwt_refresh_processor(
        self, jwt_general: JWTGeneralTokenProcessor
    ) -> JWTRefreshTokenProcessor:
        return JWTRefreshTokenProcessor(
            expire_days=self.configs.jwt.refresh_expire_days,
            token_type=self.configs.jwt.refresh_token_type,
            jwt_general=jwt_general,
        )

    @provide
    def provide_jwt_processor(
        self,
        access_token_processor: JWTAccessTokenProcessor,
        refresh_token_processor: JWTRefreshTokenProcessor,
    ) -> JWTTokenProcessor:
        return JWTTokenProcessor(
            access_token_processor=access_token_processor,
            refresh_token_processor=refresh_token_processor,
        )
