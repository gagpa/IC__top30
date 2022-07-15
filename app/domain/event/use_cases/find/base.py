from abc import ABC, abstractmethod
from uuid import UUID

from domain.event.entity import EventEntity


class FindEvent(ABC):

    @abstractmethod
    async def find(self, event_id: UUID) -> EventEntity:
        """Найти событие"""
