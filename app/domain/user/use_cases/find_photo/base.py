from abc import ABC, abstractmethod
from uuid import UUID


class FindPhoto(ABC):

    @abstractmethod
    async def find(self, user_id: UUID) -> bytes:
        """Найти"""