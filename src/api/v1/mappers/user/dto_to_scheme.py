from api.v1.schemes.user.user_create import UserCreateScheme
from api.v1.schemes.user.user_read import UserReadScheme, UserListScheme
from application.dto.user.user_create import UserCreateDTO
from application.dto.user.user_read import UserReadDTO, UserListDTO


class UserDTOToSchemeMapper:
    @staticmethod
    def to_read_scheme(dto: UserReadDTO) -> UserReadScheme:
        return UserReadScheme(
            id=dto.id,
            username=dto.username,
            is_active=dto.is_active,
            is_superuser=dto.is_superuser,
            email=dto.email,
            image_path=dto.image_path,
        )

    @staticmethod
    def to_list_scheme(dto: UserListDTO) -> UserListScheme:
        return UserListScheme(
            id=dto.id,
            username=dto.username,
            image_path=dto.image_path,
        )

    @staticmethod
    def to_create_scheme(dto: UserCreateDTO) -> UserCreateScheme:
        return UserCreateScheme(
            username=dto.username,
            email=dto.email,
            password=dto.password,
            image=dto.image,
        )
