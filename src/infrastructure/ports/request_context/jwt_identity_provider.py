from dataclasses import dataclass

from application.errors.user import AuthenticationError
from domain.entities.user.models import UserId
from infrastructure.managers.jwt import JWTTokenManager


@dataclass
class JWTIdentityProvider:
    jwt_token_manager: JWTTokenManager

    def get_current_user_id(self) -> UserId:
        token: str | None = self.jwt_token_manager.get_access_token_from_request()
        if token is None:
            raise AuthenticationError("Not authenticated")

        self.jwt_token_manager.validate_access_token_scheme(token)
        token: str = self.jwt_token_manager.remove_auth_scheme_from_token(token)
        user_id: UserId = self.jwt_token_manager.get_subject_id_from_token(token)
        if user_id is None:
            raise AuthenticationError("Not authenticated")
        return user_id
