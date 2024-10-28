from PIL import Image, UnidentifiedImageError

from fastapi import Depends, HTTPException, status, UploadFile
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from jwt.exceptions import InvalidTokenError
from starlette.status import HTTP_400_BAD_REQUEST

from src.database import database
from . import utils
from .schemas import UserLogin, UserRead
from .models import User
from src.config import settings

http_bearer = HTTPBearer()


async def validate_auth_user(
    credentials: UserLogin,
    session: AsyncSession = Depends(
        database.session_dependency,
    ),
):
    unathed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
    )
    if credentials.email:
        stmt = select(User).where(
            User.email == credentials.email,
            User.is_confirmed == True,
        )
    else:
        stmt = select(User).where(
            User.username == credentials.username,
            User.is_confirmed == True,
        )
    result = await session.execute(stmt)
    if not (user := result.scalar_one_or_none()):
        raise unathed_exc

    if not utils.validate_password(
        password=credentials.password,
        hashed_password=user.password,
    ):
        raise unathed_exc

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The account is blocked.",
        )

    return user


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    session: AsyncSession = Depends(
        database.session_dependency,
    ),
) -> User:
    token = credentials.token
    try:
        payload = utils.decode_jwt(token=token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalid.",
        )
    if payload.get("type") != settings.jwt.access_token_type:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token type incorrect: expected access token.",
        )
    user = await session.get(User, payload["sub"])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found.",
        )
    return user


def get_current_active_user(user: User = Depends(get_current_user)):
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is inactive.",
        )
    return user


async def get_validated_image_file(file: UploadFile):
    try:
        image = Image.open(file.file)
        image.verify()
    except UnidentifiedImageError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File not image"
        )
    return file
