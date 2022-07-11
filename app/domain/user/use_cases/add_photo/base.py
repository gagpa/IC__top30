from abc import ABC, abstractmethod

from uuid import UUID


class AddPhoto(ABC):

    @abstractmethod
    async def add(self, user_id: UUID, photo: bytes):
        """Добавить фотографию"""
