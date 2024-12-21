import logging
from dataclasses import dataclass

from application.dto.other.jwt import JWTRefreshDTO, JWTTokenDTO
from application.errors.user import AuthenticationError
from application.services.user.checker import UserCheckerService
from domain.entities.user.models import UserId
from infrastructure.processors.jwt_processor import JWTTokenProcessor

logger = logging.getLogger(__name__)


@dataclass
class RefreshTokenService:
    jwt_processor: JWTTokenProcessor
    user_checker_service: UserCheckerService

    async def __call__(self, dto: JWTRefreshDTO) -> JWTTokenDTO:
        payload: dict = self.jwt_processor.validate_and_decode_refresh(
            token=dto.refresh
        )
        user_id: int | None = payload.get("id")
        if not user_id:
            logger.debug("ID is not in refresh token's payload")
            raise AuthenticationError()
        user_id: UserId = UserId(user_id)
        is_valid: bool = (
            await self.user_checker_service.check_existence_and_activation_by_id(
                user_id=user_id
            )
        )
        if not is_valid:
            raise AuthenticationError("User does not exists or is banned")

        tokens: dict = self.jwt_processor.generate_refresh_access_tokens(
            payload={"id": user_id}
        )
        return JWTTokenDTO(access=tokens["access"], refresh=tokens["refresh"])
