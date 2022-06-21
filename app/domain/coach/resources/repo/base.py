from abc import ABC
from uuid import UUID

from domain.coach.entity import CoachEntity, ListCoachEntity


class CoachRepo(ABC):
    """Репозиторий коучей"""

    async def add(self, user_id: UUID, profession: str, specialization: str, experience: str, key_specializations: str) -> CoachEntity:
        """Добавить коуча в репозиторий"""

    async def find(self, user_id: UUID) -> CoachEntity:
        """Найти коуча"""

    async def filter(self, page: int = 0) -> ListCoachEntity:
        """Отфильтровать коучов в репозитории"""
