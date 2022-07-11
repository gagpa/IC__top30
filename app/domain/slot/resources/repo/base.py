import typing
from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID
from domain.slot.entity import SlotEntity, ListSlotEntity


class SlotRepo(ABC):

    @abstractmethod
    async def add(self, coach_id: UUID, start_date: datetime, end_date: datetime) -> SlotEntity:
        """Добавить слот"""

    @abstractmethod
    async def find(self, slot_id: UUID) -> SlotEntity:
        """Найти слот"""

    @abstractmethod
    async def filter(
            self,
            start_date: typing.Optional[datetime],
            end_date: typing.Optional[datetime],
            coach_id: typing.Optional[UUID],
            student_id: typing.Optional[UUID],
            is_free: typing.Optional[bool],
            page: int = 0,
    ) -> ListSlotEntity:
        """Фильтр слотов"""
