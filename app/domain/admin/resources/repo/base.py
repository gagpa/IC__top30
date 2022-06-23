from abc import ABC, abstractmethod
from uuid import UUID

from domain.admin.entities import AdminEntity, ListAdminEntity


class AdminRepo(ABC):

    @abstractmethod
    async def add(self, user_id: UUID) -> AdminEntity:
        """Добавить"""

    @abstractmethod
    async def find(self, user_id: UUID) -> AdminEntity:
        """Найти"""

    @abstractmethod
    async def filter(self, page: int = 0) -> ListAdminEntity:
        """Отфильтровать"""
