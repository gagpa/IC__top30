import typing
from uuid import UUID

from domain.student.entity import ListStudentEntity
from domain.student.resources.student_repo import StudentRepo
from .base import FilterStudents


class FilterStudentsFromRepo(FilterStudents):
    """Бизнес логика фильтрации студентов из репозитория"""

    def __init__(self, student_repo: StudentRepo):
        self.student_repo = student_repo

    async def filter(self, coach_id: typing.Optional[UUID] = None, page: int = 0) -> ListStudentEntity:
        """Отфильтровать"""
        return await self.student_repo.filter(coach_id=coach_id, page=page)
