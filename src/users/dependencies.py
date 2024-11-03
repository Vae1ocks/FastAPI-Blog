from pathlib import Path

from fastapi import HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import database
from src.auth.models import User
from .services import get_user_by_id


async def get_user_profile_image_path_dependency(
    user_id: int,
    session: AsyncSession = Depends(
        database.session_dependency,
    ),
):
    user: User = await get_user_by_id(user_id=user_id, session=session)
    if not user.image_path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found",
        )
    image_path = Path(user.image_path)
    if not image_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found",
        )
    return image_path