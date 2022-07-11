from uuid import UUID

from domain.student.resources.service import StudentService
from domain.student.resources.coach_verifier import CoachVerifier
from .base import ChooseCoach


class ChooseCoachFree(ChooseCoach):

    def __init__(self, student_service: StudentService, coach_verifier: CoachVerifier):
        self.student_service = student_service
        self.coach_verifier = coach_verifier

    async def choose(self, student_id: UUID, coach_id: UUID):
        await self.coach_verifier.is_free(coach_id)
        await self.student_service.add_coach(student_id=student_id, coach_id=coach_id)
