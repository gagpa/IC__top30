from uuid import UUID

from domain.student.resources.personal_coach_changer import PersonalCoachChanger
from domain.student.resources.student_repo import StudentRepo
from .base import RefusePersonalCoach


class SoftRefusePersonalCoach(RefusePersonalCoach):

    def __init__(self, student_repo: StudentRepo, coach_changer: PersonalCoachChanger):
        self.student_repo = student_repo
        self.coach_changer = coach_changer

    async def refuse(self, student_id: UUID):
        student = await self.student_repo.find(student_id)
        await self.coach_changer.change(student.user_id, new_coach=None)
