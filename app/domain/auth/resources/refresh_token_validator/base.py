from abc import ABC, abstractmethod
from uuid import UUID


class RefreshTokenValidator(ABC):
    """Валдитор токена для обновления"""

    @abstractmethod
    def validate(self, user_id: UUID, refresh_token: str):
        """Провалидировать"""
