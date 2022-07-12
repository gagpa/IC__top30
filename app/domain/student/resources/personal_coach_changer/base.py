import typing
from abc import ABC, abstractmethod
from uuid import UUID

from domain.student.entity import StudentEntity

__all__ = ['PersonalCoachChanger']


class PersonalCoachChanger(ABC):

    @abstractmethod
    async def change(self, student: UUID, new_coach: typing.Optional[UUID]) -> StudentEntity:
        """Сменить личного наставника"""
