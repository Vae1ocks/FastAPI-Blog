import logging

from fastapi.requests import Request

from infrastructure.ports.request_context.access_jwt_request_handler import (
    AccessJWTTokenRequestHandler,
)
from infrastructure.types import JWTAuthScheme

logger = logging.getLogger(__name__)


class HeadersAccessJWTTokenRequestHandler(AccessJWTTokenRequestHandler):
    def __init__(self, auth_scheme: JWTAuthScheme, request: Request):
        self.auth_scheme = auth_scheme
        self.request = request

    def get_access_token_from_request(self) -> str | None:
        logger.debug("Getting access token from request")
        return self.request.headers.get("Authorization")
