import typing
from uuid import UUID

import pydantic

from api_v1.base.responses import ResponseBody


class SelfCoach(ResponseBody):
    """User - Coach"""
    id: UUID
    profession_direction: str
    specialization: str
    experience: str
    profession_competencies: str
    total_seats: int
    first_name: str
    last_name: str
    patronymic: str
    email: pydantic.EmailStr
    phone: str = pydantic.Field(
        regex='^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$',
    )
    photo: typing.Optional[str] = None


class SelfStudent(ResponseBody):
    """User - Student"""
    id: UUID
    position: str
    organization: str
    experience: str
    supervisor: str
    first_name: str
    last_name: str
    patronymic: str
    email: pydantic.EmailStr
    phone: str = pydantic.Field(
        regex='^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$',
    )
    photo: typing.Optional[str] = None


class SelfAdmin(ResponseBody):
    id: UUID
    first_name: str
    last_name: str
    patronymic: str
    email: pydantic.EmailStr
    phone: str = pydantic.Field(
        regex='^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$',
    )
    photo: typing.Optional[str] = None


class SelfResponse(ResponseBody):
    """Полная информация о коуче"""
    status: bool = True
    data: typing.Union[SelfCoach, SelfStudent, SelfAdmin]
