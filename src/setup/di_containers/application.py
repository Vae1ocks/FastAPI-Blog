from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, DependenciesContainer, Singleton

from application.services.jwt.token_validation import TokenValidationService
from application.services.user.login import LoginUsernamePasswordService
from application.services.user.user_registration import UserRegistrationService
from application.use_cases.user.login import LoginUseCase
from application.use_cases.user.registration import (
    RegistrationConfirmationUseCase,
    RegistrationUseCase,
)


class ApplicationContainer(DeclarativeContainer):
    infrastructure_container = DependenciesContainer()
    db_container = DependenciesContainer()

    user_registration_service: UserRegistrationService = Factory(
        UserRegistrationService,
        password_hasher=infrastructure_container.password_hasher,
        image_checker=infrastructure_container.image_checker,
        image_loader=infrastructure_container.image_loader,
    )

    user_registration_usecase: RegistrationUseCase = Factory(
        RegistrationUseCase,
        registration_service=user_registration_service,
        code_generator=infrastructure_container.code_generator,
        email_sender=infrastructure_container.email_sender,
        uow=db_container.uow,
    )

    user_confirmation_usecase: RegistrationConfirmationUseCase = Factory(
        RegistrationConfirmationUseCase,
        registration_service=user_registration_service,
        uow=db_container.uow,
    )

    token_validation_service: TokenValidationService = Singleton(
        TokenValidationService,
        jwt_processor=infrastructure_container.jwt_processor,
    )
    login_service: LoginUsernamePasswordService = Singleton(
        LoginUsernamePasswordService,
        jwt_processor=infrastructure_container.jwt_processor,
        password_hasher=infrastructure_container.password_hasher,
    )
    login_usecase: LoginUseCase = Factory(
        LoginUseCase,
        uow=db_container.uow,
        login_service=login_service,
        token_validation_service=token_validation_service,
    )
