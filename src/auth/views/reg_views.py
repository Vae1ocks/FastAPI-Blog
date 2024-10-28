from fastapi import APIRouter, Depends, status, Request, HTTPException, UploadFile, Form
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import EmailStr

from src.auth.dependencies import get_validated_image_file
from src.database import database
from src.auth.schemas import UserRead, CreateUser, CodeScheme
from src.auth.services import (
    registrate_not_verified_user_and_send_code,
    confirm_user,
    compare_expected_session_code_and_provided,
)

router = APIRouter(
    prefix="/reg",
    tags=["Registration"],
)


@router.post("/user_data", status_code=status.HTTP_201_CREATED)
async def registration_user_data_input(
    request: Request,
    username: str = Form(min_length=3, max_length=25),
    email: EmailStr = Form(),
    password: str = Form(min_length=8),
    file = Depends(get_validated_image_file),
    session: AsyncSession = Depends(
        database.session_dependency,
    ),
):
    data = CreateUser(
        username=username,
        email=email,
        password=password,
    )
    user_id, code = await registrate_not_verified_user_and_send_code(
        data=data,
        file=file,
        session=session,
    )
    request.session["registration"] = {"user_id": user_id, "confirmation_code": code}
    return {"detail": "Continue the registration"}


@router.post("/confirmation", response_model=UserRead)
async def registration_confirmation(
    request: Request,
    code: CodeScheme,
    session: AsyncSession = Depends(
        database.session_dependency,
    ),
):
    reg_data = request.session.get("registration")
    if not reg_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Registration data is not provided",
        )
    compare_expected_session_code_and_provided(
        data=reg_data,
        provided_code=code.code,
    )

    user = await confirm_user(user_id=reg_data["user_id"], session=session)
    return user
