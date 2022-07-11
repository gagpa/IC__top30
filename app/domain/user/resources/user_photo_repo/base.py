import typing
from abc import ABC
from uuid import UUID


class UserPhotoRepo(ABC):

    async def add(self, user_id: UUID, photo: bytes):
        """Добавить фотографию"""

    async def find(self, user_id: UUID) -> bytes:
        """Найти главную фотографию (аватарку) пользователя"""

    async def filter(self, user_id: typing.Optional[UUID] = None) -> typing.List[bytes]:
        """Фильтр фотографий"""
