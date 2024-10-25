import jwt
import bcrypt
import random
from datetime import datetime, timedelta, UTC

from fastapi.exceptions import HTTPException
from fastapi import status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src import User
from .tasks import send_mail_code
from src.config import settings


def encode_jwt(
    payload: dict,
    secret: str = settings.jwt.secret,
    algorithm: str = settings.jwt.algorithm,
    expire_minutes: int = settings.jwt.access_token_lifespan_minutes,
    expire_timedelta: timedelta | None = None,
) -> str:
    to_encode = payload.copy()
    now = datetime.now(UTC)
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(iat=now, exp=expire)
    encoded = jwt.encode(to_encode, secret, algorithm=algorithm)
    return encoded


def decode_jwt(
    token: str | bytes,
    key: str = settings.jwt.secret,
    algorithm: str = settings.jwt.algorithm,
) -> dict:
    decoded = jwt.decode(token, key, algorithms=[algorithm])
    return decoded


def get_token_payload(token: str) -> dict:
    return decode_jwt(token)


# def create_access_token_by_payload(
#     payload: dict,
#     expire_minutes: int = settings.jwt.access_token_lifespan_minutes,
#     expire_timedelta: timedelta | None = None,
# ) -> str:
#     payload["type"] = settings.jwt.access_token_type
#     return encode_jwt(
#         payload=payload,
#         expire_minutes=expire_minutes,
#         expire_timedelta=expire_timedelta,
#     )


async def get_active_user(
    user_id: int,
    session: AsyncSession,
) -> User:
    stmt = select(User).where(
        User.id == user_id,
        User.is_active == True,
    )
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        raise ValueError("User not found")
    return user


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)


def validate_password(
    password: str,
    hashed_password: str,
) -> bool:
    return bcrypt.checkpw(
        password.encode(),
        hashed_password.encode(),
    )


def send_random_code_to_email(email: str) -> int:
    code = random.randint(100000, 999999)
    send_mail_code.delay(email=email, code=code)
    return code
