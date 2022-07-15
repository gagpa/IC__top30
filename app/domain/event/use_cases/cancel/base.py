from abc import ABC, abstractmethod
from uuid import UUID


class CancelEvent(ABC):

    @abstractmethod
    async def cancel(self, event_id: UUID):
        """Отменить событие"""
