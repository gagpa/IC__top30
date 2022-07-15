from datetime import datetime, timedelta
from uuid import UUID

from domain.event.resources.deleter import EventDeleter
from domain.event.resources.repo import EventRepo
from .base import CancelEvent


class CancelEventAsCoach(CancelEvent):

    def __init__(self, event_deleter: EventDeleter, event_repo: EventRepo):
        self.event_deleter = event_deleter
        self.event_repo = event_repo

    async def cancel(self, event_id: UUID):
        event = await self.event_repo.find(event_id=event_id)
        if event.start_date - datetime.now() > timedelta(hours=24):
            await self.event_deleter.delete(event_id=event_id)
