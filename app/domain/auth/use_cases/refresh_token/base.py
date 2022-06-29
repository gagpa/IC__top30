from abc import ABC
from uuid import UUID

from domain.auth.entity import AuthToken


class RefreshToken(ABC):
    """Обновить токен"""

    async def refresh(self, user_id: UUID, role: str, refresh_token: str) -> AuthToken:
        """Обновить"""
