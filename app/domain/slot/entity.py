from datetime import datetime
from uuid import UUID

from helpers.base_entity import BaseEntity
from helpers.paginated_list import PaginatedList

__all__ = [
    'SlotEntity',
    'ListSlotEntity',
]


class SlotEntity(BaseEntity):
    id: UUID
    start_date: datetime
    end_date: datetime
    coach_id: UUID


ListSlotEntity = PaginatedList[SlotEntity]
