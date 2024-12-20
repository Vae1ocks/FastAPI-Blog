import logging
from dataclasses import dataclass

from application.errors.user import AuthenticationError
from application.ports.user.identity_provider import IdentityProvider
from domain.entities.user.models import UserId
from infrastructure.managers.jwt import JWTTokenManager

logger = logging.getLogger(__name__)


@dataclass
class JWTIdentityProvider(IdentityProvider):
    jwt_token_manager: JWTTokenManager

    def get_current_user_id(self) -> UserId:
        logger.debug("Getting user's access token")
        token: str | None = self.jwt_token_manager.get_access_token_from_request()
        if token is None:
            logger.debug("Token is None")
            raise AuthenticationError("Not authenticated")

        self.jwt_token_manager.validate_access_token_scheme(token)
        token: str = self.jwt_token_manager.remove_auth_scheme_from_token(token)
        user_id: UserId = self.jwt_token_manager.get_subject_id_from_token(token)
        if user_id is None:
            logger.debug("User id is None, AuthenticationError")
            raise AuthenticationError("Not authenticated")
        return user_id
