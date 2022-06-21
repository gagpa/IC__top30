from abc import ABC, abstractmethod

from domain.user.entity import ListUserEntity


class FilterUser(ABC):
    """Класс для получения отфильтрованных пользователей"""

    @abstractmethod
    async def filter(self, page: int = 0) -> ListUserEntity:
        """Отфильтровать пользователей"""
