import typing
from abc import ABC, abstractmethod
from uuid import UUID


class UpdateAdmin(ABC):

    @abstractmethod
    async def update(
            self,
            admin_id: UUID,
            has_access: typing.Optional[bool] = None,
            first_name: typing.Optional[str] = None,
            last_name: typing.Optional[str] = None,
            patronymic: typing.Optional[str] = None,
            phone: typing.Optional[str] = None,
            photo: typing.Optional[str] = None,
    ):
        """Обновить"""
