import typing
from abc import ABC, abstractmethod
from uuid import UUID

import pydantic


class CoachUpdater(ABC):

    @abstractmethod
    async def update(
            self,
            coach_id: UUID,
            has_access: typing.Optional[bool] = None,
            first_name: typing.Optional[str] = None,
            last_name: typing.Optional[str] = None,
            patronymic: typing.Optional[str] = None,
            phone: typing.Optional[str] = None,
            photo: typing.Optional[str] = None,
            email: typing.Optional[pydantic.EmailStr] = None,
            profession_direction: typing.Optional[str] = None,
            specialization: typing.Optional[str] = None,
            experience: typing.Optional[str] = None,
            profession_competencies: typing.Optional[str] = None,
            total_seats: typing.Optional[int] = None,
    ):
        """Оьбновить"""
