from uuid import UUID

from domain.event.resources.deleter import EventDeleter
from domain.event.resources.repo import EventRepo
from domain.student.resources.personal_coach_changer import PersonalCoachChanger
from domain.student.resources.student_repo import StudentRepo
from .base import RefusePersonalStudent


class SoftRefusePersonalStudent(RefusePersonalStudent):

    def __init__(
            self,
            student_repo: StudentRepo,
            coach_changer: PersonalCoachChanger,
            event_deleter: EventDeleter,
            event_repo: EventRepo,
    ):
        self.student_repo = student_repo
        self.coach_changer = coach_changer
        self.event_deleter = event_deleter
        self.event_repo = event_repo

    async def refuse(self, student_id: UUID):
        student = await self.student_repo.find(student_id)
        events = await self.event_repo.filter(student_id=student_id, coach_id=None)
        for event in events.items:
            await self.event_deleter.delete(event.id)
        await self.coach_changer.change(student.user_id, new_coach=None)
