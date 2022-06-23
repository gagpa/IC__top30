from abc import ABC, abstractmethod
from uuid import UUID

from domain.auth.entity import Role

__all__ = ['AuthorizationService']


class AuthorizationService(ABC):

    @abstractmethod
    async def auth(self, user_id: UUID) -> Role:  # TODO: заменить на пермишены
        """Авторизовать пользователя"""
