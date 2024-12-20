from dataclasses import dataclass
from datetime import datetime, timedelta, UTC
import jwt
import logging

from application.errors.user import TokenInvalid
from infrastructure.types import JWTSecret, JWTAlgorithm

logger = logging.getLogger(__name__)


@dataclass
class JWTGeneralTokenProcessor:
    secret: JWTSecret
    algorithm: JWTAlgorithm

    def encode_jwt(self, payload: dict):
        encoded: str = jwt.encode(payload, self.secret, algorithm=self.algorithm)
        return encoded

    def decode_jwt(self, token: str | bytes) -> dict:
        logger.debug("Decoding jwt: started")
        try:
            decoded = jwt.decode(token, self.secret, algorithms=[self.algorithm])
            logger.debug("Decoding jwt: success")

        except jwt.ExpiredSignatureError:
            logger.debug("Decoding jwt: failed. ExpiredSignatureError")
            raise TokenInvalid("Token invalid")

        except jwt.InvalidTokenError:
            logger.debug("Decoding jwt: success. InvalidTokenError")
            raise TokenInvalid("Token invalid")

        logger.debug("Decoding jwt: finished")
        return decoded


@dataclass
class JWTAccessTokenProcessor:
    expire_minutes: int
    token_type: str
    jwt_general: JWTGeneralTokenProcessor

    def encode_jwt(self, payload: dict) -> str:
        logger.debug("Encoding access jwt: started")
        to_encode = payload.copy()
        now = datetime.now(UTC)
        expire = now + timedelta(minutes=self.expire_minutes)
        to_encode.update(iat=now, exp=expire, type=self.token_type)
        logger.debug("Encoding access jwt: finished")
        return self.jwt_general.encode_jwt(payload=to_encode)

    def validate_and_decode(self, token: str | bytes) -> dict:
        logger.debug("Validating and decoding jwt access started")
        decoded: dict = self.jwt_general.decode_jwt(token=token)
        if decoded["type"] != self.token_type:
            logger.debug("Decoded token's type does not match to access token's type")
            raise TokenInvalid("Token invalid")
        logger.debug("Validating and decoding jwt access finished")
        return decoded


@dataclass
class JWTRefreshTokenProcessor:
    expire_days: int
    token_type: str
    jwt_general: JWTGeneralTokenProcessor

    def encode_jwt(self, payload: dict) -> str:
        logger.debug("Encoding refresh jwt: started")
        to_encode = payload.copy()
        now = datetime.now(UTC)
        expire = now + timedelta(minutes=self.expire_days)
        to_encode.update(iat=now, exp=expire, type=self.token_type)
        logger.debug("Encoding refresh jwt: started")
        return self.jwt_general.encode_jwt(payload=to_encode)

    def validate_and_decode(self, token: str | bytes) -> dict:
        logger.debug("Validating and decoding refresh started")
        decoded: dict = self.jwt_general.decode_jwt(token=token)
        if decoded["type"] != self.token_type:
            logger.debug("Decoded token's type does not match to refresh token's type")
            raise TokenInvalid("Token invalid")
        logger.debug("Validating and decoding refresh finished")
        return decoded


@dataclass
class JWTTokenProcessor:
    access_token_processor: JWTAccessTokenProcessor
    refresh_token_processor: JWTRefreshTokenProcessor

    def generate_refresh_access_tokens(self, payload: dict):
        logger.debug("Generating refresh and access tokens: started")
        access_token: str = self.access_token_processor.encode_jwt(payload=payload)
        refresh_token: str = self.refresh_token_processor.encode_jwt(payload=payload)
        logger.debug("Generating refresh and access tokens: finished")
        return {"access": access_token, "refresh": refresh_token}
