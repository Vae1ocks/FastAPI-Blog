from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Form, status, UploadFile, Depends, HTTPException
from fastapi.requests import Request
from pydantic import EmailStr

from api.v1.mappers.user.dto_to_scheme import UserDTOToSchemeMapper
from api.v1.mappers.user.scheme_to_dto import UserSchemeToDTOMapper
from api.v1.schemes.user.user_create import UserCreateScheme
from api.v1.schemes.user.user_read import UserReadScheme
from application.dto.user.user_create import UserCreateDTO
from setup.di_containers.main import MainContainer

router = APIRouter(prefix="/reg", tags=["Registration"])


@router.post("/user-data", status_code=status.HTTP_201_CREATED)
@inject
async def user_data_input(
    request: Request,
    username: str = Form(),
    email: EmailStr = Form(),
    password: str = Form(),
    image: UploadFile | None = None,
    user_registration_usecase=Depends(Provide[
        MainContainer.application_container.user_registration_usecase
    ]),
):
    request_scheme = UserCreateScheme(
        image=image.file if image else None,
        username=username,
        email=email,
        password=password,
    )
    request_dto: UserCreateDTO = UserSchemeToDTOMapper.to_create_dto(
        scheme=request_scheme
    )
    user_dto, code = await user_registration_usecase.execute(dto=request_dto)
    request.session["registration"] = {
        "user_id": user_dto.id,
        "confirmation_code": code,
    }
    response: UserReadScheme = UserDTOToSchemeMapper.to_read_scheme(dto=user_dto)
    return response
