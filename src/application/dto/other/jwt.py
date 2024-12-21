from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class JWTTokenDTO:
    access: str
    refresh: str


@dataclass(frozen=True, slots=True)
class JWTAccessDTO:
    access: str | bytes


@dataclass(frozen=True, slots=True)
class JWTRefreshDTO:
    refresh: str | bytes
