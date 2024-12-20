from abc import ABC, abstractmethod

from domain.entities.user.models import UserId


class IdentityProvider(ABC):
    @abstractmethod
    async def get_current_user_id(self) -> UserId:
        """
        :raises AuthenticationError:
        """
