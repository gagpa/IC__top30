from uuid import UUID

from domain.student.entity import StudentEntity
from domain.student.resources.student_repo import StudentRepo
from .base import AddStudent

__all__ = ['AddStudentInRepo']


class AddStudentInRepo(AddStudent):
    """Бизнес логика, добавления студента в репозиторий"""

    def __init__(self, student_repo: StudentRepo):
        self.student_repo = student_repo

    async def add(
            self, user_id: UUID, position: str, organization: str, experience: str, supervisor: str,
    ) -> StudentEntity:
        return await self.student_repo.add(
            user_id=user_id,
            position=position,
            organization=organization,
            experience=experience,
            supervisor=supervisor,
        )
