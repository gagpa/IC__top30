from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID

from domain.event.entity import EventEntity


class MoveEvent(ABC):

    @abstractmethod
    async def move(self, event_id: UUID, new_start_date: datetime) -> EventEntity:
        """Передвинуть эвент"""
