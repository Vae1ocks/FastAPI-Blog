import logging
from dataclasses import dataclass

from application.errors.user import TokenInvalid
from domain.entities.user.models import UserId
from infrastructure.ports.request_context.access_jwt_request_handler import (
    AccessJWTTokenRequestHandler,
)
from infrastructure.processors.jwt_processor import JWTTokenProcessor
from infrastructure.types import JWTAuthScheme

logger = logging.getLogger(__name__)


@dataclass
class JWTTokenManager:
    jwt_processor: JWTTokenProcessor
    jwt_access_request_handler: AccessJWTTokenRequestHandler
    auth_scheme: JWTAuthScheme

    def get_access_token_from_request(self):
        return self.jwt_access_request_handler.get_access_token_from_request()

    def validate_access_token_scheme(self, token: str| bytes) -> None:
        logger.debug("Checking token auth scheme")
        if not token.startswith(self.auth_scheme + " "):
            logger.debug(f"Token's auth scheme is not {self.auth_scheme}")
            raise TokenInvalid()

    def remove_auth_scheme_from_token(self, token: str| bytes):
        logger.debug("Removing auth_scheme from token")
        return token[len(self.auth_scheme + " ") :]

    def get_subject_id_from_token(self, token: str | bytes) -> UserId | None:
        logger.debug("Getting subject_id from token")
        payload: dict = self.jwt_processor.access_token_processor.validate_and_decode(
            token=token
        )
        user_id: int | None = payload.get("id")

        return UserId(user_id) if user_id else None

    def get_subject_id_from_request_token(self) -> UserId:
        token: str | bytes = self.get_access_token_from_request()
        self.validate_access_token_scheme(token)
        token: str = self.remove_auth_scheme_from_token(token=token)
        return self.get_subject_id_from_token(token=token)
