from uuid import UUID

from api_v1.base.responses import ResponseBody
from helpers.paginated_list import PaginatedList
from datetime import datetime

class Event(ResponseBody):
    id: UUID
    start: datetime  #  TODO: будет int после правок фронт части
    end: datetime
    student_id: UUID


EventList = PaginatedList[Event]


class FilterEventResponse(ResponseBody):
    success: bool = True
    data: EventList
