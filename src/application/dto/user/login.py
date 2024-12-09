from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LoginUsernamePasswordDTO:
    username: str
    password: str
