from uuid import UUID

from domain.coach.entity import CoachEntity
from domain.coach.resources.repo import CoachRepo
from .base import AddCoach

__all__ = ['AddCoachInRepo']


class AddCoachInRepo(AddCoach):
    """Бизнес логика, добавления коуча в репозиторий"""

    def __init__(self, coach_repo: CoachRepo):
        self.coach_repo = coach_repo

    async def add(
            self, user_id: UUID, profession: str, specialization: str, experience: str, key_specializations: str,
    ) -> CoachEntity:
        return await self.coach_repo.add(
            user_id=user_id,
            profession=profession,
            specialization=specialization,
            experience=experience,
            key_specializations=key_specializations,
        )
