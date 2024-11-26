from domain.entities.user.models import User
from application.dto.user.user_read import UserReadDTO


class UserToDTOMapper:
    @staticmethod
    def to_read_dto(user: User) -> UserReadDTO:
        return UserReadDTO(
            id=user.id,
            username=user.username,
            is_active=user.is_active,
            is_superuser=user.is_superuser,
            email=user.email,
            image_path=user.image_path,
        )
