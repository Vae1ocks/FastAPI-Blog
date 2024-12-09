from api.v1.schemes.other.jwt import JWTTokenScheme
from application.dto.other.jwt import JWTTokenDTO


class JWTTokenSchemeToDTOMapper:
    @staticmethod
    def to_access_refresh_dto(scheme: JWTTokenScheme) -> JWTTokenDTO:
        return JWTTokenDTO(access=scheme.access, refresh=scheme.refresh)
