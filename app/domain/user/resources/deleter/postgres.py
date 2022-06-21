from uuid import UUID

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres import models
from .base import UserDeleter


class PostgresUserDeleter(UserDeleter):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def delete(self, id: UUID):
        query = delete(models.User).where(models.User.uuid == id)
        await self.session.execute(query)
