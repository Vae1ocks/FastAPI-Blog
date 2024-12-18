from fastapi.requests import Request

from application.errors.user import AuthorizationError
from infrastructure.ports.request_context.access_jwt_request_handler import (
    AccessJWTTokenRequestHandler,
)
from infrastructure.types import JWTAuthScheme


class HeadersAccessJWTTokenRequestHandler(AccessJWTTokenRequestHandler):
    def __init__(self, auth_scheme: JWTAuthScheme, request: Request):
        self.auth_scheme = auth_scheme
        self.request = request

    def get_access_token_from_request(self) -> str | None:
        return self.request.headers.get("Authorization")

    def get_validated_access_token_from_request(self) -> str:
        auth_header = self.get_access_token_from_request()

        if not auth_header:
            raise AuthorizationError("Not authorized")

        start_scheme = self.auth_scheme + " "
        if not auth_header.startswith(start_scheme):
            raise AuthorizationError("Invalid authorization credentials")

        return auth_header[len(start_scheme) :]
