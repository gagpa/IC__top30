from domain.coach.entity import ListCoachEntity
from domain.coach.resources.repo import CoachRepo
from .base import FilterCoaches


class FilterAllCoaches(FilterCoaches):
    """Бизнес логика фильтрации коучов из репозитория"""
    def __init__(self, coach_repo: CoachRepo):
        self.coach_repo = coach_repo

    async def filter(self, page: int = 0) -> ListCoachEntity:
        """Отфильтровать"""
        return await self.coach_repo.filter(page=page)
