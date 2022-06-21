from abc import ABC
from uuid import UUID

__all__ = ['DeleteUser']


class DeleteUser(ABC):
    """Бизнес логика удаления пользователя"""

    async def delete(self, id: UUID):
        """Удалить пользователя"""
