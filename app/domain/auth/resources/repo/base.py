from abc import ABC, abstractmethod
from uuid import UUID

from domain.auth.entity import AuthToken, AuthTokensList

__all__ = ['TokenRepo']


class TokenRepo(ABC):

    @abstractmethod
    async def add(self, user_id: UUID, access_token: str, refresh_token) -> AuthToken:
        """Добавить токен в репозиторий"""

    @abstractmethod
    async def find(self, user_id: UUID) -> AuthToken:
        """Найти токены авторизации"""

    @abstractmethod
    async def filter(self, page: int = 0) -> AuthTokensList:
        """Отфильтровать токены авторизации"""
