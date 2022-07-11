from abc import ABC, abstractmethod
from uuid import UUID


class CoachVerifier(ABC):

    @abstractmethod
    async def is_free(self, coach_id: UUID):
        """Проверить свободен коуч или нет"""
