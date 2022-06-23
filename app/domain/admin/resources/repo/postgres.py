from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import errors
from db.postgres import models
from domain.admin.entities import AdminEntity, ListAdminEntity
from .base import AdminRepo


class PostgresAdminRepo(AdminRepo):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, user_id: UUID) -> AdminEntity:
        query = select(models.Admin).join(models.User).where(models.User.uuid == user_id)
        cursor = await self.session.execute(query)
        if cursor.one_or_none():
            raise errors.EntityAlreadyExist
        query_user = select(models.User).where(models.User.uuid == user_id)
        cursor = await self.session.execute(query_user)
        user = cursor.one()[0]
        new_admin = models.Admin(user_id=user.id)
        self.session.add(new_admin)
        return AdminEntity(user_id=user.id)

    async def find(self, user_id: UUID) -> AdminEntity:
        pass

    async def filter(self, page: int = 0) -> ListAdminEntity:
        pass
