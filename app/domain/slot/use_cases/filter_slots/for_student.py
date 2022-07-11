from uuid import UUID

from domain.slot.entity import ListSlotEntity
from domain.slot.resources.repo import PostrgesSlotRepo
from .base import FilterSlots

__all__ = ['FilterSlotsForStudent']


class FilterSlotsForStudent(FilterSlots):

    def __init__(self, slot_repo: PostrgesSlotRepo):
        self.slot_repo = slot_repo

    async def filter(self, user_id: UUID, page: int = 0) -> ListSlotEntity:
        return await self.slot_repo.filter(
            start_date=None,
            end_date=None,
            coach_id=None,
            student_id=user_id,
            is_free=None,
            page=page,
        )
