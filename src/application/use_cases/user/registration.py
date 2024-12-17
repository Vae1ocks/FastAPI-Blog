from dataclasses import dataclass

from application.commiter import Commiter
from application.dto.other.int_code import ConfirmationCodesDTO
from application.dto.user.user_read import UserReadDTO
from application.mappers.user.user_to_dto import UserToDTOMapper
from application.dto.user.user_create import UserCreateDTO
from application.processors.code_generator import RandomCodeGenerator
from application.processors.email_sender import MailSender
from application.services.user.user_registration import UserRegistrationService
from application.uow import UnitOfWork
from domain.entities.user.models import User


@dataclass
class RegistrationUseCase:
    registration_service: UserRegistrationService
    code_generator: RandomCodeGenerator
    mail_sender: MailSender
    commiter: Commiter

    async def execute(self, dto: UserCreateDTO) -> tuple[UserReadDTO, int]:
            user: User = await self.registration_service.register_unconfirmed(
                data=dto
            )
            code = self.code_generator()
            message = f"Your confirmation code to process the registration: {code}"
            task = self.mail_sender.send(
                targets=[user.email],
                subject="Confirmation code",
                message=message,
            )
            user_dto = UserToDTOMapper.to_read_dto(user)
            await self.commiter.commit()
            return user_dto, code


@dataclass
class RegistrationConfirmationUseCase:
    registration_service: UserRegistrationService
    commiter: Commiter

    async def execute(self, dto: ConfirmationCodesDTO) -> UserReadDTO:
        user = await self.registration_service.confirm_user(data=dto)
        user_dto = UserToDTOMapper.to_read_dto(user)
        await self.commiter.commit()
        return user_dto
