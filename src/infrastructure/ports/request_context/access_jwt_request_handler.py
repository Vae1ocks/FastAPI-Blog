from abc import ABC, abstractmethod


class AccessJWTTokenRequestHandler(ABC):
    @abstractmethod
    def get_access_token_from_request(self) -> str | None: ...

    @abstractmethod
    def get_validated_access_token_from_request(self) -> str: ...