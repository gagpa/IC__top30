from abc import ABC, abstractmethod
from uuid import UUID

from domain.coach.entity import CoachEntity

__all__ = ['AddCoach']


class AddCoach(ABC):
    """Добавить коуча"""

    @abstractmethod
    async def add(
            self, user_id: UUID, profession: str, specialization: str, experience: str, key_specializations: str,
    ) -> CoachEntity:
        """Добавить"""
