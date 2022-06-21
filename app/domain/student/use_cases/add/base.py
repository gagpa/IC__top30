from abc import ABC, abstractmethod
from uuid import UUID

from domain.student.entity import StudentEntity

__all__ = ['AddStudent']

class AddStudent(ABC):
    """Добавить студента"""

    @abstractmethod
    async def add(self, user_id: UUID, position: str, organization: str, experience: str, lead: str) -> StudentEntity:
        """Добавить"""
