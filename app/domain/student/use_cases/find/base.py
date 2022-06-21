from abc import ABC
from uuid import UUID

from domain.student.entity import StudentEntity


class FindStudent(ABC):
    """Класс для поиска студента"""

    async def find(self, user_id: UUID) -> StudentEntity:
        """Найти студента"""
