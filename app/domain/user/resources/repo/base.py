import typing
from abc import ABC, abstractmethod
from uuid import UUID

import pydantic

from domain.user.entity import UserEntity


class UserRepo(ABC):
    """Класс для управления репозиторием пользователей"""

    @abstractmethod
    async def add(
            self,
            password: str,
            first_name: str,
            last_name: str,
            phone: str,
            email: pydantic.EmailStr,
            photo: typing.Optional[str] = None,
    ) -> UserEntity:
        """Добавить пользователя в репозиторий"""

    async def find(self, id: UUID):
        """Найти пользователя в репозитории"""

    async def filter(self, page: int = 0):
        """Отфильтровать пользователей в репозитории"""
