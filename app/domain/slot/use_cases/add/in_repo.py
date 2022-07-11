from datetime import datetime
from uuid import UUID

from domain.slot.entity import SlotEntity
from domain.slot.resources.repo import SlotRepo
from .base import AddSlot

__all__ = ['AddSlotInRepo']


class AddSlotInRepo(AddSlot):

    def __init__(self, slot_repo: SlotRepo):
        self.slot_repo = slot_repo

    async def add(self, coach_id: UUID, start_date: datetime, end_date: datetime) -> SlotEntity:
        return await self.slot_repo.add(coach_id=coach_id, start_date=start_date, end_date=end_date)
