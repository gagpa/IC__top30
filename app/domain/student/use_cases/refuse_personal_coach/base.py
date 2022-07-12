from abc import ABC, abstractmethod

from uuid import UUID


class RefusePersonalCoach(ABC):
    """Абстрактный класс для отказа от личного наставника"""

    @abstractmethod
    async def refuse(self, coach: UUID):
        """Отказаться от наставника"""
