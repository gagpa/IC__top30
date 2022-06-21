from abc import ABC, abstractmethod
from uuid import UUID

__all__ = ['UserDeleter']


class UserDeleter(ABC):
    """Ресурс для удаления пользователя"""

    @abstractmethod
    async def delete(self, id: UUID):
        """Удалить пользователя"""
