from datetime import datetime
from uuid import UUID

from domain.event.entity import EventEntity
from domain.event.resources.repo import EventRepo
from domain.slot.resources.repo import SlotRepo
from .base import AddEvent


class AddEventAsStudent(AddEvent):

    def __init__(self, event_repo: EventRepo, slot_repo: SlotRepo):
        self.event_repo = event_repo
        self.slot_repo = slot_repo

    async def add(self, start_date: datetime, end_date: datetime, student_id: UUID) -> EventEntity:
        return await self.event_repo.add(start_date=start_date, end_date=end_date, student_id=student_id)
