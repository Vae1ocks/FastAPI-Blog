from api.v1.schemes.user.user_create import UserCreateScheme
from api.v1.schemes.user.user_read import UserReadScheme
from application.dto.user.user_create import UserCreateDTO
from application.dto.user.user_read import UserReadDTO


class UserSchemeToDTOMapper:
    @staticmethod
    def to_read_dto(scheme: UserReadScheme) -> UserReadDTO:
        return UserReadDTO(
            id=scheme.id,
            username=scheme.username,
            is_active=scheme.is_active,
            is_superuser=scheme.is_superuser,
            email=scheme.email,
            image_path=scheme.image_path,
        )

    @staticmethod
    def to_create_dto(scheme: UserCreateScheme) -> UserCreateDTO:
        return UserCreateDTO(
            username=scheme.username,
            email=scheme.email,
            password=scheme.password,
            image=scheme.image,
        )