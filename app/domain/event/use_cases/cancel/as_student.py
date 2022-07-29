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
        time_for_event = event.start_date - datetime.now()
        if time_for_event != abs(time_for_event):
            return
        if time_for_event < timedelta(hours=24):
            await self.event_status_changer.change(status=EventStatus.burned, event_id=event_id)
        else:
            await self.event_deleter.delete(event_id=event_id)
