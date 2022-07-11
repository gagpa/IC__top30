from abc import ABC, abstractmethod
from uuid import UUID


class UserPhotoDeleter(ABC):

    @abstractmethod
    async def delete(self, user_id: UUID):
        """Удалить фотографию пользователя"""
