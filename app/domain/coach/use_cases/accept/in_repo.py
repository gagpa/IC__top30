from uuid import UUID

from domain.coach.resources.updater import CoachUpdater
from .base import AcceptCoach


class AcceptCoachInRepo(AcceptCoach):

    def __init__(self, coach_updater: CoachUpdater):
        self.coach_updater = coach_updater

    async def accept(self, coach_id: UUID):
        await self.coach_updater.update(coach_id=coach_id, has_access=True)
