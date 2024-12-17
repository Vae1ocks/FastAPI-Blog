from dataclasses import dataclass

from application.commiter import Commiter
from application.errors.user import TokenInvalid
from application.uow import UnitOfWork
from domain.entities.user.models import User
from domain.repositories.user_repository import UserRepository
from infrastructure.processors.jwt_processor import JWTTokenProcessor


@dataclass
class TokenValidationService:
    jwt_processor: JWTTokenProcessor
    user_repository: UserRepository

    async def validate_access(self, token: str) -> User:
        payload = self.jwt_processor.access_token_processor.validate_and_decode(
            token=token
        )
        user: User | None = await self.user_repository.get_by_id(user_id=payload["id"])
        if user is None:
            raise TokenInvalid()
        return user
