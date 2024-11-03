from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import FileResponse

from .dependencies import get_user_profile_image_path_dependency

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/{user_id}/profile_image", response_class=FileResponse)
async def get_user_profile_image(
    image_path=Depends(get_user_profile_image_path_dependency),
):
    return FileResponse(image_path)
