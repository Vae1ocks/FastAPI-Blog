from dataclasses import dataclass

from application.dto.user.login import LoginUsernamePasswordDTO
from application.errors.user import (
    AlreadyAuthenticatedError,
    AuthorizationError,
    AuthenticationError,
)
from application.providers.password_hasher import PasswordHasher
from application.uow import UnitOfWork
from domain.entities.user.models import User
from infrastructure.providers.jwt_processor import JWTTokenProcessor


@dataclass
class LoginUsernamePasswordService:
    jwt_processor: JWTTokenProcessor
    password_hasher: PasswordHasher

    async def __call__(self, uow, dto: LoginUsernamePasswordDTO) -> dict:
        user: User | None = await uow.user_repository.get_by_username(username=dto.username)
        if user is None:
            raise AuthorizationError("Not valid login credentials")

        if not self.password_hasher.verify(
            raw_password=dto.password,
            hashed_password=user.password,
        ):
            raise AuthenticationError("Not valid login credentials")

        token_data: dict = self.jwt_processor.generate_refresh_access_tokens(
            payload={"id": user.id}
        )
        return token_data
