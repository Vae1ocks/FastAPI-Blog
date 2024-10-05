from fastapi import APIRouter, Depends, status, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import database
from .schemas import CreateUser
from .utils import registrate_not_verified_user


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
    user_id = registrate_not_verified_user(
        data=data,
        session=session,
    )
    request.session['registration_user_id'] = user_id
    return {"detail": "continue the registration"}
