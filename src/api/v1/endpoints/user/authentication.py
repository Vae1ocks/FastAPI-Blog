from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter

from api.v1.mappers.user.scheme_to_dto import UserSchemeToDTOMapper
from api.v1.schemes.user.login import LoginScheme
from application.use_cases.user.login import LoginUseCase

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login")
@inject
async def login(
    data: LoginScheme,
    login_usecase: FromDishka[LoginUseCase],
):
    dto = UserSchemeToDTOMapper.to_login_dto(scheme=data)
    tokens: dict = await login_usecase.execute(dto=dto)
    return tokens
