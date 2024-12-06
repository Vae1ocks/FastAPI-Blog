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
        return f"User not found by {self.email=}"

    def __str__(self) -> str:
        return self.message


@dataclass
class UserUsernameNotFoundError(ApplicationError):
    username: str

    @property
    def message(self) -> str:
        return f"User not found by {self.username=}"

    def __str__(self) -> str:
        return self.message


@dataclass
class UserEmailAlreadyExistsError(ApplicationError):
    email: str

    @property
    def message(self) -> str:
        return f"User with {self.email=} already exists"

    def __str__(self) -> str:
        return self.message


@dataclass
class UserUsernameAlreadyExistsError(ApplicationError):
    username: str

    @property
    def message(self) -> str:
        return f"User with {self.username=} already exists"

    def __str__(self) -> str:
        return self.message


@dataclass
class UserUsernameEmailAlreadyExistsError(ApplicationError):
    email: str
    username: str

    @property
    def message(self) -> str:
        return f"User with {self.username=} and {self.email=} already exists"

    def __str__(self) -> str:
        return self.message
