from dataclasses import dataclass

from domain.repositories.user_repository import UserRepository
from domain.entities.user.models import User, UserId


@dataclass
class UserService:
    repository: UserRepository