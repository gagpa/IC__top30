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
            self,
            user_id: UUID,
            profession_direction: str,
            specialization: str,
            experience: str,
            profession_competencies: str,
            total_seats: int,
    ) -> CoachEntity:
        return await self.coach_repo.add(
            user_id=user_id,
            profession_direction=profession_direction,
            specialization=specialization,
            experience=experience,
            profession_competencies=profession_competencies,
            total_seats=total_seats,
        )
