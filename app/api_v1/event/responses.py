from uuid import UUID

from api_v1.base.responses import ResponseBody
from helpers.paginated_list import PaginatedList


class Student(ResponseBody):
    id: UUID
    first_name: str
    last_name: str
    patronymic: str


class Coach(ResponseBody):
    id: UUID
    first_name: str
    last_name: str
    patronymic: str


class Event(ResponseBody):
    id: UUID
    start: int
    end: int
    student: Student
    coach: Coach


EventList = PaginatedList[Event]


class FilterEventResponse(ResponseBody):
    success: bool = True
    data: EventList


class FindEventResponse(ResponseBody):
    success: bool = True
    data: Event
