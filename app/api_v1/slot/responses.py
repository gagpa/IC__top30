from uuid import UUID

from api_v1.base.responses import ResponseBody
from helpers.paginated_list import PaginatedList


class Slot(ResponseBody):
    id: UUID
    start_date: int
    end_date: int


SlotList = PaginatedList[int]


class FilterSlotResponse(ResponseBody):
    success: bool = True
    data: SlotList
