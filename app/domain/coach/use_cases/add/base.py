from abc import ABC, abstractmethod
from uuid import UUID

from domain.coach.entity import CoachEntity

__all__ = ['AddCoach']


class AddCoach(ABC):
    """Добавить коуча"""

    @abstractmethod
    async def add(
            self,
            user_id: UUID,
            profession_direction: str,
            specialization: str,
            experience: str,
            profession_competencies: str,
            total_seats: int,
    ) -> CoachEntity:
        """Добавить"""
