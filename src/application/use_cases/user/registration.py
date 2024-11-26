from dataclasses import dataclass

from application.dto.other.int_code import ConfirmationCodesDTO
from application.dto.user.user_read import UserReadDTO
from application.mappers.user.user_to_dto import UserToDTOMapper
from application.dto.user.user_create import UserCreateDTO
from application.providers.code_generator import RandomCodeGenerator
from application.services.user_registration import UserRegistrationService
from application.uow import UnitOfWork
from infrastructure.providers.email_sender import EmailSender


@dataclass
class RegistrationUseCase:
    registration_service: UserRegistrationService
    user_to_dto_mapper: UserToDTOMapper
    code_generator: RandomCodeGenerator
    email_sender: EmailSender
    uow: UnitOfWork

    async def registrate_unconfirmed(self, dto: UserCreateDTO) -> tuple[UserReadDTO, int]:
        async with self.uow as uow:
            user = await self.registration_service.register_unconfirmed(
                uow=uow, data=dto
            )
            code = self.code_generator()
            message = f"Your confirmation code to process the registration: {code}"
            self.email_sender.send(
                emails=[user.email],
                subject="Confirmation code",
                message=message,
            )
            user_dto = self.user_to_dto_mapper.to_read_dto(user)
            return user_dto, code

    async def confirm_registration(self, dto: ConfirmationCodesDTO) -> UserReadDTO:
        async with self.uow as uow:
            user = await self.registration_service.confirm_user(uow=uow, data=dto)
            user_dto = self.user_to_dto_mapper.to_read_dto(user)
            return user_dto
