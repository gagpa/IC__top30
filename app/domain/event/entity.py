from datetime import datetime
from enum import Enum
from uuid import UUID

from helpers.base_entity import BaseEntity
from helpers.paginated_list import PaginatedList


class EventStatus(Enum):
    burned = 'burned'
    active = 'active'


class EventEntity(BaseEntity):
    id: UUID
    student: UUID
    start_data: datetime
    end_date: datetime
    status: EventStatus


ListEventEntity = PaginatedList[EventEntity]
