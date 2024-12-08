from dataclasses import dataclass

from application.common.error import ApplicationError


class AuthorizationError(ApplicationError):
    pass


class AuthenticationError(ApplicationError):
    pass


class AlreadyAuthenticatedError(ApplicationError):
    pass


@dataclass
class UserEmailNotFoundError(ApplicationError):
    email: str

    @property
    def message(self) -> str:
        return f"User not found by email={self.email}"

    def __str__(self) -> str:
        return self.message


@dataclass
class UserUsernameNotFoundError(ApplicationError):
    username: str

    @property
    def message(self) -> str:
        return f"User not found by username={self.username}"

    def __str__(self) -> str:
        return self.message


@dataclass
class UserEmailAlreadyExistsError(ApplicationError):
    email: str

    @property
    def message(self) -> str:
        return f"User with email={self.email} already exists"

    def __str__(self) -> str:
        return self.message


@dataclass
class UserUsernameAlreadyExistsError(ApplicationError):
    username: str

    @property
    def message(self) -> str:
        return f"User with username={self.username} already exists"

    def __str__(self) -> str:
        return self.message


@dataclass
class UserUsernameEmailAlreadyExistsError(ApplicationError):
    email: str
    username: str

    @property
    def message(self) -> str:
        return (
            f"User with username={self.username} and email={self.email} already exists"
        )

    def __str__(self) -> str:
        return self.message
