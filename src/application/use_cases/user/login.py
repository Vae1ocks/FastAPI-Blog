from dataclasses import dataclass

from application.dto.user.login import LoginUsernamePasswordDTO
from application.errors.user import AuthorizationError, TokenInvalid
from application.services.jwt.token_validation import TokenValidationService
from application.services.user.login import LoginUsernamePasswordService
from domain.entities.user.models import User


@dataclass
class LoginUseCase:
    login_service: LoginUsernamePasswordService
    token_validation_service: TokenValidationService

    async def execute(self, dto: LoginUsernamePasswordDTO, token: str | None = None):
        if token is not None:
            try:
                user: User = await self.token_validation_service.validate_access(
                    token=token
                )
                if user is not None:
                    raise AuthorizationError("You are already authorized")
            except TokenInvalid:
                pass
        tokens: dict = await self.login_service(dto=dto)
        return tokens
