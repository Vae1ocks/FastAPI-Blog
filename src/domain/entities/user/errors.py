from domain.entities.common.errors import DomainError


class UserAlreadyActiveError(DomainError):
    message = "User is already active"

    def __str__(self) -> str:
        return self.message


class UserAlreadyConfirmedError(DomainError):
    message = "User is already confirmed"

    def __str__(self) -> str:
        return self.message


class UserAlreadyDeactivatedError(DomainError):
    message = "User is already deactivated"

    def __str__(self) -> str:
        return self.message
