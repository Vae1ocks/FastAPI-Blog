from fastapi import APIRouter, Depends, status, Request, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import database
from .schemas import UserRead, CreateUser, Code
from .utils import registrate_not_verified_user, confirm_user


router = APIRouter(
    prefix="/reg",
    tags=["Registration"],
)


@router.post("/user_data", status_code=status.HTTP_201_CREATED)
async def registration_user_data_input(
    request: Request,
    data: CreateUser,
    session: AsyncSession = Depends(
        database.session_dependency,
    ),
):
    user_id, code = await registrate_not_verified_user(
        data=data,
        session=session,
    )
    request.session["registration"] = {"user_id": user_id, "confirmation_code": code}
    return {"detail": "continue the registration"}


@router.post("/confirmation")
async def registration_confirmation(
    request: Request,
    code: Code,
    session: AsyncSession = Depends(
        database.session_dependency,
    ),
):
    reg_data_exception = HTTPException(
        status.HTTP_400_BAD_REQUEST,
        "registration data is not provided",
    )

    reg_data = request.session.get("registration")
    if not reg_data:
        raise reg_data_exception
    exp_code = reg_data.get("confirmation_code")
    user_id = reg_data.get("user_id")
    if not exp_code or not user_id:
        raise reg_data_exception

    if exp_code != code.code:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Code mismatch",
        )

    user = await confirm_user(user_id=user_id, session=session)
    user_read = UserRead.model_validate(user)
    return user_read
