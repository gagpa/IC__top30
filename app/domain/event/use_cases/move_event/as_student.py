from datetime import datetime
from uuid import UUID
from domain.event.entity import EventEntity
from domain.event.resources.mover import EventMover
from domain.event.resources.repo import EventRepo
from .base import MoveEvent


class MoveEventAsStudent(MoveEvent):

    def __init__(self, event_mover: EventMover, event_repo: EventRepo):
        self.event_repo = event_repo
        self.event_mover = event_mover

    async def move(self, event_id: UUID, new_start_date: datetime) -> EventEntity:
        event = await self.event_repo.find(event_id=event_id)
        return await self.event_mover.move(event_id=event.id, new_start_date=new_start_date)
