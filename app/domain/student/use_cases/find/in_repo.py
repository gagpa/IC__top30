from uuid import UUID

from domain.student.entity import StudentEntity
from domain.student.resources.repo import StudentRepo
from .base import FindStudent

__all__ = ['FindStudentInRepo']


class FindStudentInRepo(FindStudent):
    """Бизнес логика, поиска студента в репозитории"""
    def __init__(self, student_repo: StudentRepo):
        self.student_repo = student_repo

    async def find(self, user_id: UUID) -> StudentEntity:
        """Найти"""
        return await self.student_repo.find(user_id=user_id)
