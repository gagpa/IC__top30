from uuid import UUID

from api_v1.base.responses import ResponseBody
from domain.event.entity import EventStatus


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
    status: EventStatus
    student: Student
    coach: Coach


class FindEventResponse(ResponseBody):
    success: bool = True
    data: Event
