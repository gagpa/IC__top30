import typing
from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID

__all__ = ['DeleteSlot']


class DeleteSlot(ABC):

    @abstractmethod
    async def delete(self, coach_id: UUID, dates: typing.List[datetime]):
        pass
