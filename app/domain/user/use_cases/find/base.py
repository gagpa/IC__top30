from abc import ABC

from domain.user.entity import UserEntity

__all__ = ['FindUser']


class FindUser(ABC):
    """Бизнес логика поиска существующего пользователя"""

    async def find(self, id) -> UserEntity:
        """Найти пользователя"""
