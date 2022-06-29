from abc import ABC, abstractmethod

from uuid import UUID


class AcceptCoach(ABC):

    @abstractmethod
    async def accept(self, coach_id: UUID):
        """Принять коуча"""
