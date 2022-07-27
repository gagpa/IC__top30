import typing

import pydantic
from fastapi import File

from api_v1.base.client_requests import RequestBody


class SignUpAsUserRequest(RequestBody):
    email: pydantic.EmailStr
    password: str
    first_name: str
    last_name: str
    patronymic: str
    phone: str = pydantic.Field(
        regex='^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$',
    )
    photo: typing.Union[bytes, None] = File(default=None)


class SignUpAsStudentRequest(SignUpAsUserRequest):
    position: str
    organization: str
    experience: str
    supervisor: str


class SignUpAsCoachRequest(SignUpAsUserRequest):
    profession_direction: str
    specialization: str
    experience: str
    profession_competencies: str
    total_seats: int
