from abc import ABC, abstractmethod
from uuid import UUID
import typing
from domain.event.entity import ListEventEntity


class FilterEvents(ABC):

    @abstractmethod
    async def filter(self, user_id: UUID, student_id: typing.Optional[UUID], page: int = 0) -> ListEventEntity:
        """Фильтрация эвентов"""
