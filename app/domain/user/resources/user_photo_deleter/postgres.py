from uuid import UUID

import sqlalchemy as sql
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres import models
from .base import UserPhotoDeleter


class PostgresUserPhotoDeleter(UserPhotoDeleter):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def delete(self, user_id: UUID):
        subquery = sql.select(models.User.id).where(models.User.uuid == user_id).subquery()
        query = sql.delete(models.Photo).where(models.Photo.user_id == subquery)
        await self.session.execute(query)
