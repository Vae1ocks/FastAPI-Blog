from dataclasses import dataclass

from application.errors.user import TokenInvalid
from infrastructure.ports.request_context.access_jwt_request_handler import (
    AccessJWTTokenRequestHandler,
)
from infrastructure.processors.jwt_processor import JWTTokenProcessor


@dataclass
class JWTTokenManager:
    jwt_processor: JWTTokenProcessor
    jwt_access_request_handler: AccessJWTTokenRequestHandler

    def get_subject_id_from_token(self) -> int:
        access_token: str = (
            self.jwt_access_request_handler.get_validated_access_token_from_request()
        )
        payload: dict = self.jwt_processor.access_token_processor.validate_and_decode(
            token=access_token
        )
        user_id: int | None = payload.get("user_id")

        if not user_id:
            raise TokenInvalid("Token invalid")

        return user_id
