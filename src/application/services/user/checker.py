from dataclasses import dataclass

from application.commiter import Commiter
from domain.entities.user.models import UserId
from domain.repositories.user_repository import UserRepository


@dataclass
class UserCheckerService:
    user_repository: UserRepository
    commiter: Commiter

    async def check_existence_by_id(self, user_id: int) -> bool:
        user = await self.user_repository.get_by_id(user_id=UserId(user_id))
        return True if user else False
