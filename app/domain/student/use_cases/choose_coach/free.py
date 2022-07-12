from uuid import UUID

from domain.student.resources.personal_coach_changer import PersonalCoachChanger
from domain.student.resources.coach_verifier import CoachVerifier
from .base import ChooseCoach


class ChooseCoachFree(ChooseCoach):

    def __init__(self, personal_coach_changer: PersonalCoachChanger, coach_verifier: CoachVerifier):
        self.personal_coach_changer = personal_coach_changer
        self.coach_verifier = coach_verifier

    async def choose(self, student_id: UUID, coach_id: UUID):
        await self.coach_verifier.is_free(coach_id)
        await self.personal_coach_changer.change(student=student_id, new_coach=coach_id)
