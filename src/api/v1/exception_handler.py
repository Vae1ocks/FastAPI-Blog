from fastapi import status
import pydantic

from application.errors.article import ArticleTitleNotFound
from application.errors.common.validation import ObjectNotExistsError, AlreadyExistsError, FileNotImageError
from application.errors.user import AuthenticationError, AlreadyAuthenticatedError, AuthorizationError, \
    UserUsernameEmailAlreadyExistsError, UserEmailAlreadyExistsError, UserUsernameAlreadyExistsError, \
    UserEmailNotFoundError, UserUsernameNotFoundError


class ExceptionMessageProvider:
    @staticmethod
    def get_exception_message(exc: Exception, status_code: int) -> str:
        return "Internal Server Error" if status_code == 500 else str(exc)


class ExceptionMapper:
    def __init__(self) -> None:
        self.exception_status_code_map: dict[type[Exception], int] = {
            pydantic.ValidationError: status.HTTP_400_BAD_REQUEST,
            FileNotImageError: status.HTTP_400_BAD_REQUEST,
            AuthenticationError: status.HTTP_401_UNAUTHORIZED,
            AlreadyAuthenticatedError: status.HTTP_401_UNAUTHORIZED,
            AuthorizationError: status.HTTP_403_FORBIDDEN,
            UserUsernameEmailAlreadyExistsError: status.HTTP_409_CONFLICT,
            UserUsernameAlreadyExistsError: status.HTTP_409_CONFLICT,
            UserEmailAlreadyExistsError: status.HTTP_409_CONFLICT,
            AlreadyExistsError: status.HTTP_409_CONFLICT,
            ObjectNotExistsError: status.HTTP_404_NOT_FOUND,
            ArticleTitleNotFound: status.HTTP_404_NOT_FOUND,
            UserEmailNotFoundError: status.HTTP_404_NOT_FOUND,
            UserUsernameNotFoundError: status.HTTP_404_NOT_FOUND,
        }
