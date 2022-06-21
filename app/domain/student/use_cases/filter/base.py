import typing
from abc import ABC
from uuid import UUID

from domain.student.entity import ListStudentEntity

__all__ = ['FilterStudents']


class FilterStudents(ABC):
    """Класс для фильтрации студентов"""

    async def filter(self, coach_id: typing.Optional[UUID] = None, page: int = 0) -> ListStudentEntity:
        """Отфильтровать"""
