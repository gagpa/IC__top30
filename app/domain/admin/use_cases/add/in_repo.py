from uuid import UUID

from domain.admin.resources.repo import AdminRepo
from .base import AddAdmin


class AddAdminInRepo(AddAdmin):

    def __init__(self, admin_repo: AdminRepo):
        self.admin_repo = admin_repo

    async def add(self, user_id: UUID):
        await self.admin_repo.add(user_id=user_id)
