from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Request

from api.v1.mappers.user.scheme_to_dto import UserSchemeToDTOMapper
from api.v1.schemes.user.login import LoginScheme
from application.use_cases.user.login import LoginUseCase
from setup.di_containers.main import MainContainer

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login")
@inject
async def login(
    data: LoginScheme,
    request: Request,
    login_usecase: FromDishka[LoginUseCase],
):
    auth: str = request.headers.get("Authorization")
    token = None
    if auth:
        print('if')
        parts = auth.split()
        token = parts[1] if len(parts) == 2 else None
    dto = UserSchemeToDTOMapper.to_login_dto(scheme=data)
    tokens: dict = await login_usecase.execute(dto=dto, token=token)
    return tokens
