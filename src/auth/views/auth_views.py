from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.database import database
from src.auth.schemas import UserLogin, TokenInfo
from src.auth.utils import create_access_token, create_refresh_token
from src.auth.dependencies import validate_auth_user


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/login")
async def login(user: User = Depends(validate_auth_user)):
    access_token = create_access_token(user=user)
    refresh_token = create_refresh_token(user=user)
    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
    )
