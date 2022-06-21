from domain.user.entity import ListUserEntity
from domain.user.resources.repo import UserRepo
from .base import FilterUser

__all__ = ['FilterUserInRepo']


class FilterUserInRepo(FilterUser):
    """Класс для фильтрации пользователей в репозитории"""

    def __init__(self, user_repo: UserRepo):
        self.user_repo = user_repo

    async def filter(self, page: int = 0) -> ListUserEntity:
        """Отфильтровать пользователей"""
        return await self.user_repo.filter(page=page)
