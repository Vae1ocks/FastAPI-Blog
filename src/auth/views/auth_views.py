from fastapi import APIRouter, Depends, Body, Request, HTTPException, status
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
    hash_password,
)
from src.auth.services import (
    create_access_token,
    create_refresh_token,
    refresh_access_token,
    get_active_user_by_email_or_username,
    compare_expected_session_code_and_provided,
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


@router.post("/password-reset")
async def password_reset_send_mail(
    request: Request,
    user_data: UserEmailOrUsername,
    session: AsyncSession = Depends(database.session_dependency),
):
    """
    Первый этап сброса пароля: высылает письмо с кодом подтверждения
    на электронную почту. Нужно передать хотя бы 1 параметр: email или username,
    оба значения передавать нет необходимости.
    """
    user: User = await get_active_user_by_email_or_username(
        **user_data.model_dump(), session=session
    )
    code: int = send_random_code_to_email(email=user.email)
    request.session["password_reset"] = {
        "user_id": user.id,
        "confirmation_code": code,
    }
    return {"detail": "Confirmation code sent to your email"}


@router.post("/password-reset/set-password")
async def password_reset_set_new_password(
    request: Request,
    data: PasswordAndCodeScheme,
    session: AsyncSession = Depends(database.session_dependency),
):
    """
    Второй этап сброса пароля: ввод кода, высланного на почту
    в результате первого этапа, ввод нового пароля.
    """

    reset_data = request.session.get("password_reset")
    if not reset_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Complete first stage of password reset",
        )
    compare_expected_session_code_and_provided(
        data=reset_data,
        provided_code=data.code,
    )

    user = await session.get(User, reset_data["user_id"])
    user.password = hash_password(data.password).decode()
    await session.commit()
    return {"detail": "Password changed"}
