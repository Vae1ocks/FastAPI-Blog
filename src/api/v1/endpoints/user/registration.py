from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Form, status, UploadFile, Depends, HTTPException, Body
from fastapi.requests import Request
from pydantic import EmailStr

from api.v1.mappers.user.dto_to_scheme import UserDTOToSchemeMapper
from api.v1.mappers.user.scheme_to_dto import UserSchemeToDTOMapper
from api.v1.schemes.user.user_create import UserCreateScheme
from api.v1.schemes.user.user_read import UserReadScheme
from application.dto.other.int_code import ConfirmationCodesDTO
from application.dto.user.user_create import UserCreateDTO
from application.dto.user.user_read import UserReadDTO
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
    registration_usecase=Depends(
        Provide[MainContainer.application_container.user_registration_usecase]
    ),
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
    user_dto, code = await registration_usecase.execute(dto=request_dto)
    request.session["registration"] = {
        "user_id": user_dto.id,
        "confirmation_code": code,
    }
    response: UserReadScheme = UserDTOToSchemeMapper.to_read_scheme(dto=user_dto)
    return response


@router.post("/confirmation")
@inject
async def confirmation_registration(
    request: Request,
    code:int = Body(embed=True),
    confirmation_use_case=Depends(
        Provide[MainContainer.application_container.user_confirmation_usecase]
    ),
) -> UserReadScheme:
    session_not_provided_error = HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Registration credentials not provided",
        )

    reg_data = request.session.get("registration")
    if not reg_data:
        raise session_not_provided_error

    user_id = reg_data.get("user_id")
    confirmation_code = reg_data.get("confirmation_code")
    if not user_id or not confirmation_code:
        raise session_not_provided_error

    dto = ConfirmationCodesDTO(
        user_id=user_id,
        expected_code=confirmation_code,
        provided_code=code,
    )
    user_dto: UserReadDTO = await confirmation_use_case.execute(dto=dto)
    user_scheme: UserReadScheme = UserDTOToSchemeMapper.to_read_scheme(dto=user_dto)

    del request.session["registration"]
    return user_scheme
