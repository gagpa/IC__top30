from abc import ABC, abstractmethod
from uuid import UUID


class AddAdmin(ABC):

    @abstractmethod
    async def add(self, user_id: UUID):
        """Добавить"""
