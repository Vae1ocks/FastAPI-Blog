from dataclasses import dataclass

from application.dto.user.login import LoginUsernamePasswordDTO
from application.errors.user import AuthorizationError, TokenInvalid
from application.services.jwt.token_validation import TokenValidationService
from application.services.user.login import LoginUsernamePasswordService
from application.uow import UnitOfWork
from domain.entities.user.models import User


@dataclass
class LoginUseCase:
    uow: UnitOfWork
    login_service: LoginUsernamePasswordService
    token_validation_service: TokenValidationService

    async def execute(self, dto: LoginUsernamePasswordDTO, token: str | None = None):
        async with self.uow as uow:
            if token is not None:
                try:
                    user: User = await self.token_validation_service.validate_access(
                        token=token, uow=uow
                    )
                    if user is not None:
                        raise AuthorizationError("You are already authorized")
                except TokenInvalid:
                    pass

            tokens: dict = await self.login_service(uow=uow, dto=dto)
            return tokens
