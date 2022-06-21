from uuid import UUID

from domain.coach.entity import CoachEntity
from domain.coach.resources.repo import CoachRepo
from .base import FindCoach

__all__ = ['FindCoachInRepo']


class FindCoachInRepo(FindCoach):
    """Бизнес логика, поиска коуча в репозитории"""
    def __init__(self, coach_repo: CoachRepo):
        self.coach_repo = coach_repo

    async def find(self, user_id: UUID) -> CoachEntity:
        """Найти"""
        return await self.coach_repo.find(user_id=user_id)
