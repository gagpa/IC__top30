from datetime import datetime, timedelta
from uuid import UUID

from domain.event.entity import EventStatus
from domain.event.resources.deleter import EventDeleter
from domain.event.resources.repo import EventRepo
from domain.event.resources.stutus_changer import EventStatusChanger
from .base import CancelEvent


class CancelEventAsStudent(CancelEvent):

    def __init__(self, event_deleter: EventDeleter, event_status_changer: EventStatusChanger, event_repo: EventRepo):
        self.event_deleter = event_deleter
        self.event_status_changer = event_status_changer
        self.event_repo = event_repo

    async def cancel(self, event_id: UUID):
        event = await self.event_repo.find(event_id=event_id)
        print(event.start_date - datetime.now() < timedelta(hours=24))
        if event.start_date - datetime.now() < timedelta(hours=24):
            await self.event_status_changer.change(status=EventStatus.burned, event_id=event_id)
        else:
            await self.event_deleter.delete(event_id=event_id)
