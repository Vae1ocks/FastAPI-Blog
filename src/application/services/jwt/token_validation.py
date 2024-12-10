from dataclasses import dataclass

from application.uow import UnitOfWork
from domain.entities.user.models import User
from infrastructure.providers.jwt_processor import JWTTokenProcessor


@dataclass
class TokenValidationService:
    jwt_processor: JWTTokenProcessor

    async def validate_access(self, token: str, uow: UnitOfWork) -> User | None:
        payload = self.jwt_processor.access_token_processor.validate_and_decode(
            token=token
        )
        user: User | None = await uow.user_repository.get_by_id(user_id=payload["id"])
        return user
