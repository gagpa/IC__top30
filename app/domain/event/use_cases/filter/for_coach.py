import typing
from uuid import UUID

from domain.event.entity import ListEventEntity
from domain.event.resources.repo import EventRepo
from .base import FilterEvents


class FilterEventsForCoach(FilterEvents):

    def __init__(self, event_repo: EventRepo):
        self.event_repo = event_repo

    async def filter(self, user_id: UUID, student_id: typing.Optional[UUID], page: int = 0) -> ListEventEntity:
        if student_id:  # TODO: Реализовано для админа, нужна отдельная реализация поиска эвентов
            return await self.event_repo.filter(
                coach_id=None,
                student_id=student_id,
                page=page,
            )
        return await self.event_repo.filter(
            coach_id=user_id,
            student_id=student_id,
            page=page,
        )
