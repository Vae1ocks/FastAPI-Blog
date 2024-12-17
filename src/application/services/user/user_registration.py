from dataclasses import dataclass
from typing import BinaryIO

from application.commiter import Commiter
from application.dto.other.int_code import ConfirmationCodesDTO
from application.errors.common.code_mismatch import CodeMismatchError
from application.errors.user import (
    UserUsernameEmailAlreadyExistsError,
    UserUsernameAlreadyExistsError,
    UserEmailAlreadyExistsError,
)
from application.dto.user.user_create import UserCreateDTO
from application.processors.file_operators import ImageChecker, ImageLoader
from application.processors.password_hasher import PasswordHasher
from domain.entities.user.models import User, UserId
from domain.repositories.user_repository import UserRepository


@dataclass
class UserRegistrationService:
    user_repository: UserRepository
    password_hasher: PasswordHasher
    image_checker: ImageChecker
    image_loader: ImageLoader
    commiter: Commiter

    async def register_unconfirmed(self, data: UserCreateDTO) -> User:
        user: User | None = await self._validate_unique_email_and_username(
            username=data.username,
            email=data.email,
        )

        hashed_password: str = self.password_hasher.hash(
            raw_password=data.password,
        ).decode()

        image_path = None
        if data.image:
            image_path = await self._process_user_image(file=data.image)

        if user is None:
            user = User(
                email=data.email,
                username=data.username,
                password=hashed_password,
                image_path=image_path,
            )
            self.user_repository.add(user)
            await self.commiter.flush()
        return user

    async def confirm_user(self, data: ConfirmationCodesDTO):  # noqa
        if data.expected_code != data.provided_code:
            raise CodeMismatchError()

        user: User = await self.user_repository.get_by_id(user_id=UserId(data.user_id))
        user.confirm_registration()
        self.user_repository.add(user)
        return user

    async def _validate_unique_email_and_username(  # noqa
        self, username: str, email: str
    ) -> User | None:
        existing_users = await self.user_repository.get_by_email_or_username(
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
                    return user
                raise UserUsernameEmailAlreadyExistsError(
                    username=username, email=email
                )

            if user.username == username:
                raise UserUsernameAlreadyExistsError(username=username)
            raise UserEmailAlreadyExistsError(email=email)

        raise UserUsernameEmailAlreadyExistsError(username=username, email=email)

    async def _process_user_image(self, file: BinaryIO):
        self.image_checker.check(file)
        image_path = await self.image_loader(image=file)
        return image_path
