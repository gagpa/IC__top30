from uuid import UUID

from domain.user.entity import UserEntity
from domain.user.resources.repo.base import UserRepo
from .base import FindUser

__all__ = ['FindUserInRepo']


class FindUserInRepo(FindUser):
    """Бизнес логика поиска существующего пользователя в репозитории"""

    def __init__(self, user_repo: UserRepo):
        self.user_repo = user_repo

    async def find(self, id: UUID) -> UserEntity:
        """Поиск пользователя в репозитории"""
        return await self.user_repo.find(id)
