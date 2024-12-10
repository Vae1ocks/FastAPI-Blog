from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Request
from fastapi.openapi.models import HTTPBearer
from fastapi.params import Depends

from api.v1.mappers.user.scheme_to_dto import UserSchemeToDTOMapper
from api.v1.schemes.user.login import LoginScheme
from setup.di_containers.main import MainContainer

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login")
@inject
async def login(
    data: LoginScheme,
    request: Request,
    login_usecase=Depends(Provide[MainContainer.application_container.login_usecase]),
):
    auth: str = request.headers.get("Authorization")
    token = None
    if auth:
        parts = auth.split()
        token = parts[1] if len(parts) == 2 else None
    dto = UserSchemeToDTOMapper.to_login_dto(scheme=data)
    tokens: dict = await login_usecase.execute(dto=dto, token=token)
    return tokens
