from typing import Tuple

import jwt
import bcrypt
import time
import random
from datetime import datetime, timedelta, UTC

from fastapi.exceptions import HTTPException
from fastapi import status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result
from sqlalchemy.orm import Mapped

from src import User
from .schemas import CreateUser, UserRead
from .tasks import send_mail_code
from src.config import settings
from src import database


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


def create_access_token(
    user: User,
    expire_minutes: int = settings.jwt.access_token_lifespan_minutes,
    expire_timedelta: timedelta | None = None,
) -> str:
    payload = {
        "type": settings.jwt.access_token_type,
        "sub": user.id,
    }
    return encode_jwt(
        payload=payload,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta,
    )


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


def create_refresh_token(
    user: User,
    expire_timedelta: timedelta = timedelta(
        days=settings.jwt.refresh_token_lifespan_days
    ),
    expire_minutes: int | None = None,
) -> str:
    payload = {"type": settings.jwt.refresh_token_type, "sub": user.id}
    return encode_jwt(
        payload=payload,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta,
    )


async def refresh_access_token(
    refresh_token: str,
    session: AsyncSession,
) -> str:
    user = await get_current_active_user_for_refresh(
        token=refresh_token,
        session=session,
    )
    return create_access_token(user=user)


def validate_refresh_token(token: str) -> dict:
    payload = decode_jwt(token)
    if payload.get("type") != settings.jwt.refresh_token_type:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Incorrect token. Expected {settings.jwt.refresh_token_type!r}, "
            f"got {payload.get('type')!r}",
        )
    exp = payload.get("exp")
    if exp < time.time():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token incorrect."
        )
    return payload


async def get_current_active_user_for_refresh(
    token: str,
    session: AsyncSession,
) -> User:
    payload = validate_refresh_token(token)
    user = await get_active_user(
        user_id=payload["sub"],
        session=session,
    )
    return user


# async def generate_new_refresh_token(
#     token: str,
#     session: AsyncSession,
# ) -> str:
#     """
#     Перепроверяет, существует ли пользователь с указанным в payload id
#     и возвращает новый refresh_token.
#     """
#
#     payload = validate_refresh_token(token=token)
#     user_id = payload.get("sub")
#     user = await session.get(User, user_id)
#     if user is None:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED, detail="Token incorrect."
#         )
#
#     return create_refresh_token(user=user)


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
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found",
        )
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


async def registrate_not_verified_user(
    data: CreateUser,
    session: AsyncSession,
) -> tuple[int, int]:
    """
    Служит для создания пользователя с неподтверждённым email,
    отправляет код подтверждения на почту.
    """

    result = await session.execute(
        select(User).filter(User.email == data.email),
    )

    if not (user := result.scalar_one_or_none()):
        hashed_password = hash_password(data.password).decode()
        user = User(
            **data.model_dump(exclude={"password"}),
            password=hashed_password,
            is_active=True,
            is_confirmed=False,
            is_superuser=False,
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)

    elif user.is_confirmed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user already exists and is confirmed.",
        )
    code = random.randint(100000, 999999)
    send_mail_code.delay(email=data.email, code=code)
    return user.id, code


async def confirm_user(
    user_id: int,
    session: AsyncSession,
) -> User:
    user = await session.get(User, user_id)
    if user is None:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Incorrect registration data",
        )
    user.is_confirmed = True
    await session.commit()
    return user
