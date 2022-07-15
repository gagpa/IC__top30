from uuid import UUID

from domain.event.entity import ListEventEntity
from domain.event.resources.repo import EventRepo
from .base import FilterEvents


class FilterEventsForStudent(FilterEvents):

    def __init__(self, event_repo: EventRepo):
        self.event_repo = event_repo

    async def filter(self, user_id: UUID, page: int = 0) -> ListEventEntity:
        return await self.event_repo.filter(
            coach_id=None,
            student_id=user_id,
            page=page,
        )
