from dishka import Provider, provide, Scope, from_context
from fastapi import Request

from api.v1.endpoints.adapters.request_context.headers_access_jwt_request_handler import (
    HeadersAccessJWTTokenRequestHandler,
)
from application.ports.user.identity_provider import IdentityProvider
from application.processors.code_generator import RandomCodeGenerator
from application.processors.email_sender import MailSender
from application.processors.file_operators import ImageChecker, ImageLoader
from application.processors.password_hasher import PasswordHasher
from domain.repositories.user_repository import UserRepository
from infrastructure.managers.jwt import JWTTokenManager
from infrastructure.ports.request_context.access_jwt_request_handler import (
    AccessJWTTokenRequestHandler,
)
from infrastructure.ports.request_context.jwt_identity_provider import (
    JWTIdentityProvider,
)
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
from infrastructure.repositories.sqlalchemy.user_repository import UserRepositoryImpl
from infrastructure.types import PasswordPepper, JWTAlgorithm, JWTSecret, JWTAuthScheme
from setup.configs import AllConfigs


class InfrastructureRequestContextProvider(Provider):
    scope = Scope.REQUEST

    router = from_context(provides=Request)

    @provide(provides=JWTAuthScheme, scope=Scope.APP)
    def provide_jwt_auth_scheme(self, configs: AllConfigs) -> JWTAuthScheme:
        return JWTAuthScheme(configs.jwt.scheme)

    access_jwt_token_request_handler = provide(
        source=HeadersAccessJWTTokenRequestHandler,
        provides=AccessJWTTokenRequestHandler,
    )

    jwt_token_manager = provide(
        source=JWTTokenManager,
    )


class InfrastructureProvider(Provider):
    user_repository = provide(
        source=UserRepositoryImpl,
        provides=UserRepository,
        scope=Scope.REQUEST,
    )

    @provide(scope=Scope.APP)
    def provide_password_pepper(self, configs: AllConfigs) -> PasswordPepper:
        return PasswordPepper(configs.pepper.pepper)

    password_hasher = provide(
        source=BcryptPasswordHasher,
        provides=PasswordHasher,
        scope=Scope.APP,
    )

    image_checker = provide(
        source=ImageCheckerImpl, provides=ImageChecker, scope=Scope.APP
    )

    @provide(provides=ImageLoader, scope=Scope.APP)
    def provide_image_loader(self, configs: AllConfigs) -> FileSystemImageLoader:
        return FileSystemImageLoader(
            directory=configs.file.users_profile_images_directory,
            file_name_patter=configs.file.file_save_time_pattern,
        )

    @provide(provides=RandomCodeGenerator, scope=Scope.APP)
    def provide_code_generator(self, configs: AllConfigs) -> RandomIntegerCodeGenerator:
        return RandomIntegerCodeGenerator(
            min_val=configs.code_generator.min_val,
            max_val=configs.code_generator.max_val,
        )

    @provide(provides=MailSender, scope=Scope.APP)
    def provide_email_sender(self, configs: AllConfigs) -> EmailSender:
        return EmailSender(
            host=configs.smtp.host,
            host_user=configs.smtp.host_user,
            host_password=configs.smtp.host_password,
            port=configs.smtp.port,
        )

    @provide(scope=Scope.APP)
    def provide_jwt_general_processor(
        self, configs: AllConfigs
    ) -> JWTGeneralTokenProcessor:
        return JWTGeneralTokenProcessor(
            secret=JWTSecret(configs.jwt.secret),
            algorithm=configs.jwt.algorithm,
        )

    @provide(scope=Scope.APP)
    def provide_jwt_access_processor(
        self, jwt_general: JWTGeneralTokenProcessor, configs: AllConfigs
    ) -> JWTAccessTokenProcessor:
        return JWTAccessTokenProcessor(
            expire_minutes=configs.jwt.access_expire_minutes,
            token_type=configs.jwt.access_token_type,
            jwt_general=jwt_general,
        )

    @provide(scope=Scope.APP)
    def provide_jwt_refresh_processor(
        self, jwt_general: JWTGeneralTokenProcessor, configs: AllConfigs
    ) -> JWTRefreshTokenProcessor:
        return JWTRefreshTokenProcessor(
            expire_days=configs.jwt.refresh_expire_days,
            token_type=configs.jwt.refresh_token_type,
            jwt_general=jwt_general,
        )

    jwt_token_processor = provide(
        source=JWTTokenProcessor,
        scope=Scope.APP,
    )

    identity_provider = provide(
        source=JWTIdentityProvider,
        provides=IdentityProvider,
        scope=Scope.REQUEST,
    )
