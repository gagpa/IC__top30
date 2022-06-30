import typing
from uuid import UUID

from domain.admin.resources.updater import AdminUpdater
from .base import UpdateAdmin


class UpdateAdminInRepo(UpdateAdmin):

    def __init__(self, admin_updater: AdminUpdater):
        self.admin_updater = admin_updater

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
        await self.admin_updater.update(
            admin_id=admin_id,
            has_access=has_access,
            first_name=first_name,
            last_name=last_name,
            patronymic=patronymic,
            phone=phone,
            photo=photo,
        )
