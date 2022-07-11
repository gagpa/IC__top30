from abc import ABC, abstractmethod

from uuid import UUID


class ChooseCoach(ABC):

    @abstractmethod
    async def choose(self, student_id: UUID, coach_id: UUID):
        """Выбрать"""
