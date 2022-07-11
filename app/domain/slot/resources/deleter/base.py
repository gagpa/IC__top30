from abc import ABC
from datetime import datetime
from uuid import UUID


class SlotDeleter(ABC):

    async def delete(self, coach_id: UUID, start_date: datetime):
        pass
