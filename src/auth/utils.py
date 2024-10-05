from typing import Tuple

import jwt
import bcrypt
import random
from datetime import datetime, timedelta, UTC

from fastapi.exceptions import HTTPException
from fastapi import status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import Mapped

from src import User
from .schemas import CreateUser, UserRead
from .tasks import send_mail_code
from src.config import settings


def encode_jwt(
    payload: dict,
    secret: str = settings.jwt.secret,
    algorithm: str = settings.jwt.algorithm,
    expire_minutes: int = settings.jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
) -> str:
    to_encode = payload.copy()
    now = datetime.now(UTC)
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(iat=now, exp=expire)
    encoded = jwt.encode(payload, secret, algorithm=algorithm)
    return encoded


def decode_jwt(
    token: str | bytes,
    key: str = settings.jwt.secret,
    algorithm: str = settings.jwt.algorithm,
):
    decoded = jwt.decode(token, key, algorightms=[algorithm])
    return decoded


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)


def validate_password(
    password: str,
    hashed_password: bytes,
) -> bool:
    return bcrypt.checkpw(
        password.encode(),
        hashed_password,
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


async def confirm_user(user_id: int, session: AsyncSession,) -> User:
    user = await session.get(User, user_id)
    user.is_confirmed = True
    await session.commit()
    return user

