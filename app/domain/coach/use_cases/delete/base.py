from abc import ABC, abstractmethod
from uuid import UUID


class DeleteCoach(ABC):
    """Удалить коуча"""

    @abstractmethod
    async def delete(self, user_id: UUID):
        """Удалить"""
