from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class UserUpdateDTO:
    id: int
    username: str
    image_path: str


@dataclass(frozen=True, slots=True)
class UserUpdatePasswordDTO:
    id: int
    password: str


@dataclass(frozen=True, slots=True)
class UserUpdateEmailDTP:
    id: int
    email: str
