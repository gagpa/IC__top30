import typing
from uuid import UUID

import sqlalchemy as sql
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
import errors
from db.postgres import models
from .base import UserPhotoRepo


class PostgresUserPhotoRepo(UserPhotoRepo):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, user_id: UUID, photo: str):
        subquery_user = sql.select(models.User.id).where(models.User.uuid == user_id).subquery()
        query = sql.insert(models.Photo).values(user_id=subquery_user, img=photo)
        await self.session.execute(query)

    async def find(self, user_id: UUID) -> str:
        subquery_user = sql.select(models.User.id).where(models.User.uuid == user_id).subquery()
        query = sql.select(models.Photo.img).where(models.Photo.user_id == subquery_user)
        cursor = await self.session.execute(query)
        try:
            photo = cursor.one()[0]
        except NoResultFound:
            raise errors.EntityNotFounded
        return photo

    async def filter(self, user_id: typing.Optional[UUID] = None) -> typing.List[str]:
        subquery_user = sql.select(models.User.id).where(models.User.uuid == user_id).subquery()
        query = sql.select(models.Photo.img).where(models.Photo.user_id == subquery_user)
        cursor = await self.session.execute(query)
        return cursor.all()
