from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID


class EventMover(ABC):

    @abstractmethod
    async def move(self, event_id: UUID, new_start_date: datetime):
        """Подвинуть событие"""
