from datetime import datetime, timedelta
from uuid import UUID

from domain.coach.resources.deleter import CoachDeleter
from domain.event.entity import EventStatus
from domain.event.resources.deleter import EventDeleter
from domain.event.resources.repo import EventRepo
from domain.event.resources.stutus_changer import EventStatusChanger
from .base import DeleteCoach

__all__ = ['DeleteCoachFromRepo']


class DeleteCoachFromRepo(DeleteCoach):
    """Бизнес логика удаления коуча из репозитория"""

    def __init__(
            self,
            coach_deleter: CoachDeleter,
            event_repo: EventRepo,
            event_deleter: EventDeleter,
            event_status_changer: EventStatusChanger,
    ):
        self.coach_deleter = coach_deleter
        self.event_repo = event_repo
        self.event_deleter = event_deleter
        self.event_status_changer = event_status_changer

    async def delete(self, user_id: UUID):
        freeze_rim = timedelta(hours=24)
        now = datetime.now()
        events = await self.event_repo.filter(coach_id=user_id, student_id=None)
        for event in events.items:
            time_for_event = event.start_date - now
            if time_for_event > freeze_rim:
                await self.event_deleter.delete(event.id)
            elif time_for_event == abs(time_for_event):
                await self.event_status_changer.change(event.id, status=EventStatus.burned)
        await self.coach_deleter.delete(user_id)
