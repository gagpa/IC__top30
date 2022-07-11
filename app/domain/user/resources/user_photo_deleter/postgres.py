from uuid import UUID

import sqlalchemy as sql
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres import models
from .base import UserPhotoDeleter


class PostgresUserPhotoDeleter(UserPhotoDeleter):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def delete(self, user_id: UUID):
        query = sql.delete(models.Photo).join(models.User).where(models.User.uuid == user_id)
        await self.session.execute(query)
