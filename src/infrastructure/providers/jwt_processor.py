from dataclasses import dataclass
from datetime import datetime, timedelta, UTC

import jwt
from jwt import ExpiredSignatureError, InvalidTokenError

from application.errors.user import AuthorizationError, AuthenticationError
from infrastructure.types import JWTSecret, JWTAlgorithm


@dataclass
class JWTTokenProcessor:
    access_token_processor: None
    refresh_token_processor: None

    def generate_refresh_access_tokens(self, user_id: int):
        access_token: str = self.access_token_processor.encode_jwt(user_id=user_id)
        refresh_token: str = self.refresh_token_processor.encode_jwt(user_id=user_id)
        return {"access": access_token, "refresh": refresh_token}



@dataclass
class JWTGeneralTokenProcessor:
    secret: JWTSecret
    algorithm: JWTAlgorithm

    def encode_jwt(self, payload: dict):
        encoded: str = jwt.encode(payload, self.secret, algorithm=self.algorithm)
        return encoded

    def decode_jwt(self, token: str | bytes) -> dict:
        try:
            decoded = jwt.decode(token, self.secret, algorithms=[self.algorithm])
        except ExpiredSignatureError:
            raise AuthorizationError("Token invalid")
        except InvalidTokenError:
            raise AuthorizationError("Token invalid")
        return decoded



@dataclass
class JWTAccessTokenProcessor:
    expire_minutes: int
    token_type: str
    jwt_general: JWTGeneralTokenProcessor

    def encode_jwt(self, payload: dict) -> str:
        to_encode = payload.copy()
        now = datetime.now(UTC)
        expire = now + timedelta(minutes=self.expire_minutes)
        to_encode.update(iat=now, exp=expire, type=self.token_type)
        return self.jwt_general.encode_jwt(payload=to_encode)

    def validate_and_decode(self, token: str | bytes) -> dict:
        decoded: dict = self.jwt_general.decode_jwt(token=token)
        if decoded["type"] != self.token_type:
            raise AuthenticationError("Token invalid")
        return decoded


@dataclass
class JWTRefreshTokenProcessor:
    expire_days: int
    token_type: str
    jwt_general: JWTGeneralTokenProcessor

    def encode_jwt(self, payload: dict) -> str:
        to_encode = payload.copy()
        now = datetime.now(UTC)
        expire = now + timedelta(minutes=self.expire_days)
        to_encode.update(iat=now, exp=expire, type=self.token_type)
        return self.jwt_general.encode_jwt(payload=to_encode)

    def validate_and_decode(self, token: str | bytes) -> dict:
        decoded: dict = self.jwt_general.decode_jwt(token=token)
        if decoded["type"] != self.token_type:
            raise AuthenticationError("Token invalid")
        return decoded
