from abc import ABC, abstractmethod
from uuid import UUID

__all__ = ['FilterSlots']


class FilterSlots(ABC):

    @abstractmethod
    async def filter(self, user_id: UUID):
        """Отфильтровать слоты"""
