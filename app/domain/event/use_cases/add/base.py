import typing
from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID


class AddEvent(ABC):

    @abstractmethod
    async def add(self, start_date: datetime, end_date: datetime, student_id: UUID):
        """Добавить эвент"""
