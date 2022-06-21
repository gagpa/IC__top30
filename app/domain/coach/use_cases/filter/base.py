from abc import ABC

from domain.coach.entity import ListCoachEntity

__all__ = ['FilterCoachs']


class FilterCoachs(ABC):
    """Класс для фильтрации коучов"""

    async def filter(self, page: int = 0) -> ListCoachEntity:
        """Отфильтровать"""
