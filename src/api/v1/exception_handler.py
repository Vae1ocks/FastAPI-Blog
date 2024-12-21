from dataclasses import dataclass
from typing import Any

from fastapi import FastAPI, Request, status
import pydantic
from fastapi.responses import ORJSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic_core import ErrorDetails

from application.common.error import ApplicationError
from application.errors.article import ArticleTitleNotFound
from application.errors.common.code_mismatch import CodeMismatchError
from application.errors.common.validation import (
    ObjectNotExistsError,
    AlreadyExistsError,
    FileNotImageError,
)
from application.errors.user import (
    AuthenticationError,
    AlreadyAuthenticatedError,
    AuthorizationError,
    UserUsernameEmailAlreadyExistsError,
    UserEmailAlreadyExistsError,
    UserUsernameAlreadyExistsError,
    UserEmailNotFoundError,
    UserUsernameNotFoundError, TokenInvalid,
)
from domain.entities.common.errors import DomainError
from domain.entities.user.errors import UserAlreadyActiveError, UserAlreadyConfirmedError, UserAlreadyDeactivatedError


@dataclass(frozen=True, slots=True)
class ExceptionSchema:
    description: str


@dataclass(frozen=True, slots=True)
class ExceptionSchemaRich:
    description: str
    details: list[dict[str, Any]] | None = None



class ExceptionMessageProvider:
    @staticmethod
    def get_exception_message(exc: Exception, status_code: int) -> str:
        return "Internal Server Error" if status_code == 500 else str(exc)


class ExceptionMapper:
    def __init__(self) -> None:
        self.exception_status_code_map: dict[type[Exception], int] = {
            pydantic.ValidationError: status.HTTP_400_BAD_REQUEST,
            FileNotImageError: status.HTTP_400_BAD_REQUEST,
            CodeMismatchError: status.HTTP_400_BAD_REQUEST,
            AuthenticationError: status.HTTP_401_UNAUTHORIZED,
            AlreadyAuthenticatedError: status.HTTP_401_UNAUTHORIZED,
            TokenInvalid: status.HTTP_401_UNAUTHORIZED,
            AuthorizationError: status.HTTP_403_FORBIDDEN,
            UserUsernameEmailAlreadyExistsError: status.HTTP_409_CONFLICT,
            UserUsernameAlreadyExistsError: status.HTTP_409_CONFLICT,
            UserEmailAlreadyExistsError: status.HTTP_409_CONFLICT,
            AlreadyExistsError: status.HTTP_409_CONFLICT,
            ObjectNotExistsError: status.HTTP_404_NOT_FOUND,
            ArticleTitleNotFound: status.HTTP_404_NOT_FOUND,
            UserEmailNotFoundError: status.HTTP_404_NOT_FOUND,
            UserUsernameNotFoundError: status.HTTP_404_NOT_FOUND,
            UserAlreadyActiveError: status.HTTP_409_CONFLICT,
            UserAlreadyConfirmedError: status.HTTP_409_CONFLICT,
            UserAlreadyDeactivatedError: status.HTTP_409_CONFLICT,
            DomainError: status.HTTP_500_INTERNAL_SERVER_ERROR,
            ApplicationError: status.HTTP_500_INTERNAL_SERVER_ERROR,
        }

    def get_status_code(self, exc: Exception) -> int:
        return self.exception_status_code_map.get(
            type(exc), status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@dataclass
class ExceptionHandler:
    app: FastAPI
    exception_message_provider: ExceptionMessageProvider
    mapper: ExceptionMapper

    def setup_handlers(self) -> None:
        for exc_class in self.mapper.exception_status_code_map:
            self.app.add_exception_handler(exc_class, self.handle_exception)
        self.app.add_exception_handler(Exception, self.handle_unexpected_exceptions)

    async def handle_exception(self, _: Request, exc: Exception) -> ORJSONResponse:
        status_code: int = self.mapper.get_status_code(exc)
        if status_code >= 500:
            # TODO: Logging
            ...
        else:
            # TODO: Logging
            ...

        exception_message: str = self.exception_message_provider.get_exception_message(
            exc, status_code
        )
        details: list[ErrorDetails] | None = (
            exc.errors() if isinstance(exc, pydantic.ValidationError) else None
        )

        return self.create_exception_response(
            details=details,
            status_code=status_code,
            exception_message=exception_message,
        )

    def handle_unexpected_exceptions(
        self, _: Request, exc: Exception
    ) -> ORJSONResponse:
        # TODO: Logging
        exception_message: str = "Internal server error"
        return self.create_exception_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            exception_message=exception_message,
        )

    @staticmethod
    def create_exception_response(
        status_code: int,
        exception_message: str,
        details: list[ErrorDetails] | None = None,
    ) -> ORJSONResponse:
        response_content: ExceptionSchemaRich | ExceptionSchema = (
            ExceptionSchemaRich(exception_message, jsonable_encoder(details))
            if details
            else ExceptionSchema(exception_message)
        )
        return ORJSONResponse(status_code=status_code, content=response_content)
