from dishka import Provider, provide, Scope

from application.services.jwt.token_validation import TokenValidationService
from application.services.user.login import LoginUsernamePasswordService
from application.services.user.user_registration import UserRegistrationService
from application.use_cases.user.login import LoginUseCase
from application.use_cases.user.registration import (
    RegistrationUseCase,
    RegistrationConfirmationUseCase,
)


class ApplicationProvider(Provider):
    user_registration_service = provide(
        source=UserRegistrationService,
        scope=Scope.REQUEST,
    )
    user_registration_usecase = provide(
        source=RegistrationUseCase,
        scope=Scope.REQUEST,
    )
    user_confirmation_usecase = provide(
        RegistrationConfirmationUseCase,
        scope=Scope.REQUEST,
    )
    token_validation_service = provide(
        TokenValidationService,
        scope=Scope.APP,
    )
    login_service = provide(
        LoginUsernamePasswordService,
        scope=Scope.APP,
    )
    login_usecase = provide(
        LoginUseCase,
        scope=Scope.REQUEST,
    )
