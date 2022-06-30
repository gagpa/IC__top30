import typing
from abc import ABC, abstractmethod
from uuid import UUID

import pydantic


class StudentUpdater(ABC):

    @abstractmethod
    async def update(
            self,
            student_id: UUID,
            has_access: typing.Optional[bool] = None,
            first_name: typing.Optional[str] = None,
            last_name: typing.Optional[str] = None,
            patronymic: typing.Optional[str] = None,
            phone: typing.Optional[str] = None,
            email: typing.Optional[pydantic.EmailStr] = None,
            position: typing.Optional[str] = None,
            photo: typing.Optional[str] = None,
            experience: typing.Optional[str] = None,
            supervisor: typing.Optional[str] = None,
            coach_id: typing.Optional[UUID] = None,
    ):
        """Оьбновить"""
