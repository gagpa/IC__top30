from abc import ABC, abstractmethod
from uuid import UUID
from datetime import datetime

class EventMover(ABC):

    @abstractmethod
    async def move(self, event_id: UUID, new_start_date: datetime):
