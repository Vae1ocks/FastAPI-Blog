from dataclasses import dataclass

from application.commiter import Commiter
from application.dto.user.login import LoginUsernamePasswordDTO
from application.errors.user import (
    AlreadyAuthenticatedError,
    AuthorizationError,
    AuthenticationError,
)
from application.processors.password_hasher import PasswordHasher
from domain.entities.user.models import User
from domain.repositories.user_repository import UserRepository
from infrastructure.processors.jwt_processor import JWTTokenProcessor


@dataclass
class LoginUsernamePasswordService:
    user_repository: UserRepository
    jwt_processor: JWTTokenProcessor
    password_hasher: PasswordHasher
    commiter: Commiter

    async def __call__(self, dto: LoginUsernamePasswordDTO) -> dict:
        user: User | None = await self.user_repository.get_by_username(username=dto.username)
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
