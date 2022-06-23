import typing
from abc import ABC, abstractmethod
from uuid import UUID


class AuthenticationService(ABC):

    @abstractmethod
    async def auth(self, login: str) -> typing.Tuple[UUID, str]:
        """Аутентификация пользователя"""
