from dataclasses import dataclass

from application.errors.user import TokenInvalid
from domain.entities.user.models import UserId
from infrastructure.ports.request_context.access_jwt_request_handler import (
    AccessJWTTokenRequestHandler,
)
from infrastructure.processors.jwt_processor import JWTTokenProcessor
from infrastructure.types import JWTAuthScheme


@dataclass
class JWTTokenManager:
    jwt_processor: JWTTokenProcessor
    jwt_access_request_handler: AccessJWTTokenRequestHandler
    auth_scheme: JWTAuthScheme

    def get_access_token_from_request(self):
        return self.jwt_access_request_handler.get_access_token_from_request()

    def validate_access_token_scheme(self, token: str) -> None:
        if not token.startswith(self.auth_scheme + " "):
            raise TokenInvalid()

    def remove_auth_scheme_from_token(self, token: str):
        return token[len(self.auth_scheme + " ") :]

    def get_subject_id_from_token(self, token: str) -> UserId:
        payload: dict = self.jwt_processor.access_token_processor.validate_and_decode(
            token=token
        )
        user_id: int | None = payload.get("user_id")

        if not user_id:
            raise TokenInvalid("Token invalid")

        return UserId(user_id)
