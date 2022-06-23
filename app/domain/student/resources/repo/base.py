import typing
from abc import ABC
from uuid import UUID

from domain.student.entity import StudentEntity, ListStudentEntity


class StudentRepo(ABC):
    """Репозиторий студентов"""

    async def add(
            self, user_id: UUID, position: str, organization: str, experience: str, supervisor: str,
    ) -> StudentEntity:
        """Добавить студента в репозиторий"""

    async def find(self, user_id: UUID) -> StudentEntity:
        """Найти студента"""

    async def filter(self, coach_id: typing.Optional[UUID] = None, page: int = 0) -> ListStudentEntity:
        """Отфильтровать студентов в репозитории"""
