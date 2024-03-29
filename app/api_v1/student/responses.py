import typing
from uuid import UUID

import pydantic

from api_v1.base.responses import ResponseBody
from domain.auth.entity import Role
from helpers.paginated_list import PaginatedList


class UserStudent(ResponseBody):
    """User - Student"""
    id: UUID
    position: str
    organization: str
    experience: str
    supervisor: str
    coach_id: typing.Optional[UUID] = None
    role: Role = Role.STUDENT
    first_name: str
    last_name: str
    patronymic: str
    email: pydantic.EmailStr
    phone: str = pydantic.Field(
        regex='^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$',
    )
    photo: typing.Optional[str] = None
    has_access: bool


UserStudentList = PaginatedList[UserStudent]


class ListstudentsResponse(ResponseBody):
    """Список студентов"""
    status: bool = True
    data: UserStudentList


class StudentByIDResponse(ResponseBody):
    """Полная информация о студенте"""
    status: bool = True
    data: UserStudent
