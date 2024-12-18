from dishka import Provider, provide, Scope

from application.commiter import Commiter
from application.services.jwt.token_validation import TokenValidationService
from application.services.user.checker import UserCheckerService
from application.services.user.login import LoginUsernamePasswordService
from application.services.user.user_registration import UserRegistrationService
from application.use_cases.user.login import LoginUseCase
from application.use_cases.user.registration import (
    RegistrationUseCase,
    RegistrationConfirmationUseCase,
)
from infrastructure.persistence.sqlalchemy.commiter import SqlaCommiter


class ApplicationProvider(Provider):
    scope = Scope.REQUEST

    user_registration_service = provide(
        source=UserRegistrationService,
    )
    user_registration_usecase = provide(
        source=RegistrationUseCase,
    )
    user_confirmation_usecase = provide(
        RegistrationConfirmationUseCase,
    )
    user_checker_service = provide(
        source=UserCheckerService,
    )
    token_validation_service = provide(
        TokenValidationService,
    )
    login_service = provide(
        LoginUsernamePasswordService,
    )
    login_usecase = provide(
        LoginUseCase,
    )
    commiter = provide(
        source=SqlaCommiter,
        provides=Commiter,
    )
