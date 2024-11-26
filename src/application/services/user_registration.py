from dataclasses import dataclass
from io import BytesIO

from application.dto.other.int_code import ConfirmationCodesDTO
from application.uow import UnitOfWork
from application.dto.user.user_create import UserCreateDTO
from application.providers.code_generator import CodeIntGenerator
from application.providers.file_operators import ImageChecker, ImageLoader
from application.providers.password_hasher import PasswordHasher
from domain.entities.user.models import User


@dataclass
class UserRegistrationService:
    code_generator: CodeIntGenerator
    password_hasher: PasswordHasher
    image_checker: ImageChecker
    image_loader: ImageLoader

    async def register_unconfirmed(self, uow: UnitOfWork, data: UserCreateDTO) -> User:
        user = self._validate_unique_email_and_username(
            username=data.username,
            email=data.email,
        )

        hashed_password = self.password_hasher.hash(
            raw_password=data.password,
        ).decode()

        image_path = self._process_user_image(file=data.image)

        user = User(
            email=data.email,
            username=data.username,
            password=hashed_password,
            image_path=image_path,
        )

        uow.user_repository.add(user)
        return user

    async def confirm_user(self, uow: UnitOfWork, data: ConfirmationCodesDTO):  # noqa
        if data.expected_code != data.provided_code:
            raise ValueError("Code mismatch")

        user: User = await uow.user_repository.get_by_id(user_id=data.user_id)
        user.confirm_registration()
        uow.user_repository.add(user)
        return user

    async def _validate_unique_email_and_username(  # noqa
        self, uow: UnitOfWork, username: str, email: str
    ):
        existing_users = await uow.user_repository.get_by_email_or_username(
            username=username, email=email
        )
        if not existing_users:
            return

        if len(existing_users) == 1:
            # If user exists, but with the same username and email, so I suppose that
            # this user haven't finished the reg before, so just continue
            # the registration.

            user = existing_users[0]
            if user.email == email and user.username == username:
                if not user.is_confirmed and user.is_active:
                    return
                raise ValueError("User with such username and email already exists")

            text = "User with such email already exists"
            if user.username == username:
                text = "User with such username already exists"
            raise ValueError(text)

        raise ValueError("User with such username and email already exists")

    async def _process_user_image(self, file: BytesIO):
        self.image_checker(file)
        image_path = await self.image_loader(image=file)
        return image_path
