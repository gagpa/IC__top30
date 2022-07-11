from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID

from domain.slot.entity import SlotEntity

__all__ = ['AddSlot']


class AddSlot(ABC):

    @abstractmethod
    async def add(self, choach_id: UUID, start_date: datetime, end_date: datetime) -> SlotEntity:
        """Добавить слот"""
