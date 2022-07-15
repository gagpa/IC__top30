import typing
from abc import ABC, abstractmethod
from uuid import UUID
from datetime import datetime
from domain.event.entity import EventEntity, ListEventEntity


class EventRepo(ABC):

    @abstractmethod
    async def add(self, start_date: datetime, end_date: datetime, student_id: UUID) -> EventEntity:
        """Добавить новый эвент"""

    @abstractmethod
    async def find(self, event_id: UUID) -> EventEntity:
        """Найти эвент по внешнему id"""

    @abstractmethod
    async def filter(
            self,
            coach_id: typing.Optional[UUID],
            student_id: typing.Optional[UUID],
            page: int = 0,
    ) -> ListEventEntity:
        """Фильтрация эвентов"""
