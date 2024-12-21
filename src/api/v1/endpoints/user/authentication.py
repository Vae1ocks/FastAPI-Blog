from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter

from api.v1.mappers.user.scheme_to_dto import UserSchemeToDTOMapper
from api.v1.schemes.other.jwt import JWTRefreshScheme, JWTTokenScheme
from api.v1.schemes.user.login import LoginScheme
from application.dto.other.jwt import JWTRefreshDTO, JWTTokenDTO
from application.use_cases.user.login import LoginUseCase, RefreshUseCase

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


@router.post("/refresh", response_model=JWTTokenScheme)
@inject
async def refresh(
    data: JWTRefreshScheme,
    refresh_usecase: FromDishka[RefreshUseCase],
):
    dto: JWTRefreshDTO = JWTRefreshDTO(refresh=data.refresh)
    tokens_dto: JWTTokenDTO = await refresh_usecase.execute(dto=dto)
    # return JWTTokenScheme(access=tokens_dto.access, refresh=tokens_dto.refresh)
    return tokens_dto
