from abc import ABC, abstractmethod
from uuid import UUID


class StudentService(ABC):

    @abstractmethod
    async def add_coach(self, student_id: UUID, coach_id: UUID):
        """Добавить наставника"""

    @abstractmethod
    async def decline_coach(self, student_id: UUID):
        """Отклонить наставника"""
