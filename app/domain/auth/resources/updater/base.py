from abc import ABC
from uuid import UUID

from domain.auth.entity import AuthToken

__all__ = ['TokenUpdater']


class TokenUpdater(ABC):
    """Класс для обновления токена доступа."""

    async def update(self, user_id: UUID, access_token: str, refresh_token: str) -> AuthToken:
        """Обновить"""
