from domain.student.resources.deleter import StudentDeleter
from .base import DeleteStudent
from uuid import UUID

__all__ = ['DeleteStudentFromRepo']


class DeleteStudentFromRepo(DeleteStudent):
    """Бизнес логика удаления студента из репозитория"""

    def __init__(self, student_deleter: StudentDeleter):
        self.student_deleter = student_deleter

    async def delete(self, user_id: UUID):
        await self.student_deleter.delete(user_id)
