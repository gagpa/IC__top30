from abc import ABC, abstractmethod
from uuid import UUID

__all__ = ['StudentDeleter']


class StudentDeleter(ABC):
    """Ресурс для удаления студента"""

    @abstractmethod
    async def delete(self, user_id: UUID):
        """Удалить студента"""
