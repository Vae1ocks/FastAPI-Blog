from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse

from old.src.database import database
from .dependencies import get_user_profile_image_path_dependency
from .services import get_user_by_id
from old.src.users.schemas import UserRead

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/{user_id}/profile_image", response_class=FileResponse)
def get_user_profile_image(
    image_path=Depends(
        get_user_profile_image_path_dependency,
    ),
):
    return FileResponse(image_path)


@router.get("/{user_id}", response_model=UserRead)
async def user_detail(
    user_id: int,
    session=Depends(
        database.session_dependency,
    ),
):
    user = await get_user_by_id(user_id=user_id, session=session)
    return user
