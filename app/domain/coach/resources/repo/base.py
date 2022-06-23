import typing
from abc import ABC
from uuid import UUID

from domain.coach.entity import CoachEntity, ListCoachEntity


class CoachRepo(ABC):
    """Репозиторий коучей"""

    async def add(
            self,
            user_id: UUID,
            total_seats: int,
            profession_direction: str,
            specialization: str,
            experience: str,
            profession_competencies: str,
    ) -> CoachEntity:
        """Добавить коуча в репозиторий"""

    async def find(self, user_id: UUID) -> CoachEntity:
        """Найти коуча"""

    async def filter(self, is_free: typing.Optional[bool] = None, page: int = 0) -> ListCoachEntity:
        """Отфильтровать коучов в репозитории"""
