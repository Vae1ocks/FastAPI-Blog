from api.v1.schemes.other.jwt import JWTTokenScheme
from application.dto.other.jwt import JWTTokenDTO


class JWTTokenDTOToSchemeMapper:
    @staticmethod
    def to_access_refresh_scheme(dto: JWTTokenDTO) -> JWTTokenScheme:
        return JWTTokenScheme(access=dto.access, refresh=dto.refresh)
