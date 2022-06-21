import typing
from uuid import UUID

import pydantic

from helpers.paginated_list import PaginatedList


class UserStudent(pydantic.BaseModel):
    """User - Student"""
    id: UUID
    position: str
    organization: str
    experience: str
    lead: str
    first_name: str
    last_name: str
    email: pydantic.EmailStr
    phone: str = pydantic.Field(
        regex='^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$',
    )
    photo: typing.Optional[str] = None


UserStudentList = PaginatedList[UserStudent]


class ListstudentsResponse(pydantic.BaseModel):
    """Список студентов"""
    status: bool = True
    data: UserStudentList


class StudentByIDResponse(pydantic.BaseModel):
    """Полная информация о студенте"""
    status: bool = True
    data: UserStudent
