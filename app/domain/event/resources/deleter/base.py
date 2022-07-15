from abc import ABC, abstractmethod
from uuid import UUID


class EventDeleter(ABC):

    @abstractmethod
    async def delete(self, event_id: UUID):
        """Удалить эвент"""
