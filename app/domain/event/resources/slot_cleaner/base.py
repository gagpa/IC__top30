from abc import ABC, abstractmethod
from uuid import UUID


class SlotCleaner(ABC):

    @abstractmethod
    async def clean(self, event_id: UUID):
        """Отчистить"""
