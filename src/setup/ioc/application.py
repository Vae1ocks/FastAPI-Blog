from dishka import Provider, provide, Scope

from application.commiter import Commiter
from application.services.jwt.refresh import RefreshTokenService
from application.services.user.checker import UserCheckerService
from application.services.user.login import LoginUsernamePasswordService
from application.services.user.user_registration import UserRegistrationService
from application.use_cases.user.login import LoginUseCase, RefreshUseCase
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
    refresh_service = provide(
        source=RefreshTokenService,
    )
    refresh_usecase = provide(
        source=RefreshUseCase,
    )
