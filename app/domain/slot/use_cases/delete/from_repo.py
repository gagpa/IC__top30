import typing
from datetime import datetime
from uuid import UUID

from domain.slot.resources.deleter import SlotDeleter
from .base import DeleteSlot

__all__ = ['DeleteSlotFromRepo']


class DeleteSlotFromRepo(DeleteSlot):

    def __init__(self, slot_deleter: SlotDeleter):
        self.slot_deleter = slot_deleter

    async def delete(self, coach_id: UUID, dates: typing.List[datetime]):
        for date in dates:
            await self.slot_deleter.delete(coach_id, date)
