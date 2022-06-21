from uuid import UUID

from domain.user.resources.deleter import UserDeleter
from .base import DeleteUser

__all__ = ['DeleteUserFromRepo']


class DeleteUserFromRepo(DeleteUser):
    """Бизнес логика удаления пользователя"""

    def __init__(self, user_deleter: UserDeleter):
        self.user_deleter = user_deleter

    async def delete(self, id: UUID):
        """Удалить пользователя"""
        await self.user_deleter.delete(id)
