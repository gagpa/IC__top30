from abc import ABC, abstractmethod
from uuid import UUID

__all__ = ['CoachDeleter']


class CoachDeleter(ABC):
    """Ресурс для удаления коуча"""

    @abstractmethod
    async def delete(self, user_id: UUID):
        """Удалить коуча"""
