import typing
from uuid import UUID

import sqlalchemy as sql
from sqlalchemy.ext.asyncio import AsyncSession

import errors
from db.postgres import models
from .base import UserPhotoRepo


class PostgresUserPhotoRepo(UserPhotoRepo):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, user_id: UUID, photo: bytes):
        pass

    async def find(self, user_id: UUID) -> bytes:
        query = sql.select(models.User.photo).where(models.User.uuid == user_id)
        cursor = await self.session.execute(query)
        photo = cursor.one()
        if not photo:
            raise errors.EntityNotFounded
        return photo

    async def filter(self, user_id: typing.Optional[UUID] = None) -> typing.List[bytes]:
        query = sql.select(models.User.photo).where(models.User.uuid == user_id)
        cursor = await self.session.execute(query)
        return cursor.all()
