import time
from datetime import timedelta
from typing import BinaryIO

from fastapi import HTTPException
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped
from starlette import status

from old.src import User
from old.src.auth.schemas import CreateUser
from old.src.auth.utils import (
    encode_jwt,
    decode_jwt,
    get_active_user,
    hash_password,
    send_random_code_to_email,
)
from old.src.config import settings


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
    try:
        user = await get_active_user(
            user_id=payload["sub"],
            session=session,
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found",
        )
    return user


async def registrate_not_verified_user_and_send_code(
    data: CreateUser,
    file: BinaryIO,
    session: AsyncSession,
) -> tuple[Mapped[int], int]:
    """
    Служит для создания пользователя с неподтверждённым email,
    отправляет код подтверждения на почту.
    """

    result = await session.execute(
        select(User).filter(
            (User.email == data.email) | (User.username == data.username),
        ),
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
        if file is not None:
            await user.save_picture(file=file)
        session.add(user)
        await session.commit()
        await session.refresh(user)

    elif user.is_confirmed:
        repeated_value = "email" if user.email == data.email else "username"
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The user with provided {repeated_value} "
                   f"already exists and is confirmed.",
        )
    code = send_random_code_to_email(email=data.email)
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


async def get_active_user_by_email_or_username(
    session: AsyncSession,
    email: str | None = None,
    username: str | None = None,
) -> User:
    if not email and not username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Neither email nor username provided.",
        )

    stmt = select(User).where(User.is_active == True)
    if email:
        stmt = stmt.where(User.email == email)
    else:
        stmt = stmt.where(User.username == username)

    result: Result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found.",
        )

    return user


def compare_expected_session_code_and_provided(
    data: dict,
    provided_code: int,
) -> None:
    exp_code = data.get("confirmation_code")
    user_id = data.get("user_id")
    if not exp_code or not user_id:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "registration data is not provided",
        )

    if exp_code != provided_code:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Code mismatch",
        )
    return
