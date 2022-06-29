from uuid import UUID

from domain.student.resources.updater import StudentUpdater
from .base import AcceptStudent


class AcceptStudentInRepo(AcceptStudent):

    def __init__(self, student_updater: StudentUpdater):
        self.student_updater = student_updater

    async def accept(self, student_id: UUID):
        await self.student_updater.update(student_id=student_id, has_access=True)
