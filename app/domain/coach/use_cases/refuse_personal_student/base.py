from abc import ABC, abstractmethod
from uuid import UUID


class RefusePersonalStudent(ABC):

    @abstractmethod
    async def refuse(self, coach_id: UUID, student_id: UUID):
        """Отказаться от студента"""
