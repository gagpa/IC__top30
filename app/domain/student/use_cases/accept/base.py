from abc import ABC, abstractmethod

from uuid import UUID


class AcceptStudent(ABC):

    @abstractmethod
    async def accept(self, student_id: UUID):
        """Принять коуча"""
