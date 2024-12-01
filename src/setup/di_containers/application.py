from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, DependenciesContainer

from application.services.user_registration import UserRegistrationService
from application.use_cases.user.registration import (
    RegistrationConfirmationUseCase,
    RegistrationUseCase,
)


class ApplicationContainer(DeclarativeContainer):
    infrastructure_container = DependenciesContainer()
    db_container = DependenciesContainer()

    user_registration_service = Factory(
        UserRegistrationService,
        password_hasher=infrastructure_container.password_hasher,
        image_checker=infrastructure_container.image_checker,
        image_loader=infrastructure_container.image_loader,
    )

    user_registration_usecase = Factory(
        RegistrationUseCase,
        registration_service=user_registration_service,
        code_generator=infrastructure_container.code_generator,
        email_sender=infrastructure_container.email_sender,
        uow=db_container.uow,
    )

    user_confirmation_usecase = Factory(
        RegistrationConfirmationUseCase,
        registration_service=user_registration_service,
        uow=db_container.uow,
    )
