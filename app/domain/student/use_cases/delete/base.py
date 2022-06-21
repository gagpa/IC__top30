from abc import ABC, abstractmethod
from uuid import UUID


class DeleteStudent(ABC):
    """Удалить студента"""

    @abstractmethod
    async def delete(self, user_id: UUID):
        """Удалить"""
