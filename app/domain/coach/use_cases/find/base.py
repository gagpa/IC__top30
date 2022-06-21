from abc import ABC
from uuid import UUID

from domain.coach.entity import CoachEntity


class FindCoach(ABC):
    """Класс для поиска коуча"""

    async def find(self, user_id: UUID) -> CoachEntity:
        """Найти коуча"""
