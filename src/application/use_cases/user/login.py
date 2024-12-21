from dataclasses import dataclass
import logging

from application.dto.user.login import LoginUsernamePasswordDTO
from application.errors.user import (
    AuthenticationError,
    TokenInvalid,
    AlreadyAuthenticatedError,
)
from application.ports.user.identity_provider import IdentityProvider
from application.services.user.checker import UserCheckerService
from application.services.user.login import LoginUsernamePasswordService
from domain.entities.user.models import UserId

logger = logging.getLogger(__name__)


@dataclass
class LoginUseCase:
    identity_provider: IdentityProvider
    user_checker_service: UserCheckerService
    login_service: LoginUsernamePasswordService

    async def execute(self, dto: LoginUsernamePasswordDTO):
        try:
            logger.debug("Checking if user exists")
            user_id: UserId = self.identity_provider.get_current_user_id()
            if user_id is not None:
                user_is_valid: bool = (
                    await self.user_checker_service.check_existence_and_activation_by_id(
                        user_id=user_id
                    )
                )
                if user_is_valid:
                    logger.debug("Already authenticated")
                    raise AlreadyAuthenticatedError()

        except TokenInvalid:
            logger.debug("Token invalid, pass")
        except AuthenticationError:
            logger.debug("Authentication error, pass")
        tokens: dict = await self.login_service(dto=dto)
        logger.debug("Exiting from LoginUseCase")
        return tokens
