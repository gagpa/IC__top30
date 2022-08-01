from domain.student.resources.deleter import StudentDeleter
from .base import DeleteStudent
from uuid import UUID
from domain.event.resources.repo import EventRepo
from domain.event.resources.deleter import EventDeleter
__all__ = ['DeleteStudentFromRepo']


class DeleteStudentFromRepo(DeleteStudent):
    """Бизнес логика удаления студента из репозитория"""

    def __init__(self, student_deleter: StudentDeleter, event_repo: EventRepo, event_deleter: EventDeleter):
        self.student_deleter = student_deleter
        self.event_repo = event_repo
        self.event_deleter = event_deleter

    async def delete(self, user_id: UUID):
        events = await self.event_repo.filter(student_id=user_id, coach_id=None)
        for event in events.items:
            await self.event_deleter.delete(event.id)
        await self.student_deleter.delete(user_id)
