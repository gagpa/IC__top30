from abc import ABC

from domain.coach.entity import ListCoachEntity

__all__ = ['FilterCoaches']


class FilterCoaches(ABC):
    """Класс для фильтрации коучов"""

    async def filter(self, page: int = 0) -> ListCoachEntity:
        """Отфильтровать"""
