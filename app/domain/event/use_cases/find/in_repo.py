from uuid import UUID

from domain.event.entity import EventEntity
from domain.event.resources.repo import EventRepo
from .base import FindEvent


class FindEventInRepo(FindEvent):

    def __init__(self, event_repo: EventRepo):
        self.event_repo = event_repo

    async def find(self, event_id: UUID) -> EventEntity:
        return await self.event_repo.find(event_id)
