from fastapi import APIRouter, Depends, Body, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.database import database
from src.auth.schemas import (
    UserLogin,
    TokenInfo,
    UserEmailOrUsername,
    PasswordAndCodeScheme,
)
from src.auth.utils import (
    send_random_code_to_email,
)
from src.auth.services import (
    create_access_token,
    create_refresh_token,
    refresh_access_token,
    get_active_user_by_email_or_username,
)
from src.auth.dependencies import validate_auth_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/login", response_model=TokenInfo)
async def login(user: User = Depends(validate_auth_user)):
    access_token: str = create_access_token(user=user)
    refresh_token: str = create_refresh_token(user=user)
    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post(
    "/refresh",
    response_model=TokenInfo,
    response_model_exclude_none=True,
)
async def refresh(
    refresh_token: str = Body(),
    session: AsyncSession = Depends(database.session_dependency),
):
    access_token = await refresh_access_token(
        refresh_token=refresh_token,
        session=session,
    )
    return TokenInfo(access_token=access_token)
