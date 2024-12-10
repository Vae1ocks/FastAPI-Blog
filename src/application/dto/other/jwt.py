from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class JWTTokenDTO:
    access: str
    refresh: str
