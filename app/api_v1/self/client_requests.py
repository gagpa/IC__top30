import typing
from uuid import UUID
from fastapi import File
import pydantic

from api_v1.base.client_requests import RequestBody


class UserUpdateFields(RequestBody):
    first_name: typing.Optional[str] = None
    last_name: typing.Optional[str] = None
    patronymic: typing.Optional[str] = None
    phone: typing.Optional[str] = pydantic.Field(
        None,
        regex='^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$',
    )
    photo: typing.Union[bytes, None] = File(default=None)
    email: typing.Optional[pydantic.EmailStr] = None
    position: typing.Optional[str] = None
    organization: typing.Optional[str] = None
    experience: typing.Optional[str] = None
    supervisor: typing.Optional[str] = None
    profession_direction: typing.Optional[str] = None
    specialization: typing.Optional[str] = None
    profession_competencies: typing.Optional[str] = None
    total_seats: typing.Optional[int] = None
    coach_id: typing.Optional[UUID] = None
