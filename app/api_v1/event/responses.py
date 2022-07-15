from uuid import UUID

from api_v1.base.responses import ResponseBody
from helpers.paginated_list import PaginatedList


class Event(ResponseBody):
    id: UUID
    start_date: int
    end_date: int
    student_id: UUID


EventList = PaginatedList[Event]


class FilterEventResponse(ResponseBody):
    success: bool = True
    data: EventList
