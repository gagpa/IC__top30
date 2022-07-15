from abc import ABC, abstractmethod
from uuid import UUID

from domain.event.entity import EventStatus


class EventStatusChanger(ABC):

    @abstractmethod
    async def change(self, event_id: UUID, status: EventStatus):
        """Изменить статус"""
