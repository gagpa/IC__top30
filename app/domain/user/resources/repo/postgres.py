import typing
from uuid import UUID

import pydantic
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

import errors
from db.postgres import models
from domain.user.entity import UserEntity, ListUserEntity
from .base import UserRepo


class PostgresUserRepo(UserRepo):

    def __init__(self, session: AsyncSession, limit: int = 20):
        self.session = session
        self.limit = limit

    async def add(
            self,
            password: str,
            first_name: str,
            last_name: str,
            patronymic: str,
            phone: str,
            email: pydantic.EmailStr,
            photo: typing.Optional[str] = None,
    ) -> UserEntity:
        query = select(models.User).where(models.User.email == email)
        cursor = await self.session.execute(query)
        if cursor.one_or_none():
            raise errors.EntityAlreadyExist()
        new_user = models.User(
            password=password,
            first_name=first_name,
            last_name=last_name,
            patronymic=patronymic,
            phone=phone,
            email=email,
        )
        self.session.add(new_user)
        await self.session.flush()
        if photo:
            insert_photo_query = insert(models.Photo).values(img=photo, user_id=new_user.id)
            await self.session.execute(insert_photo_query)
        return UserEntity(
            id=new_user.uuid,
            first_name=new_user.first_name,
            last_name=new_user.last_name,
            patronymic=new_user.patronymic,
            phone=new_user.phone,
            email=pydantic.EmailStr(new_user.email),
            has_access=new_user.has_access,
            has_photo=bool(photo),
        )

    async def find(self, id: UUID) -> UserEntity:
        query = select(models.User, models.Photo.id). \
            join(models.Photo, models.Photo.user_id == models.User.id). \
            where(models.User.uuid == id)
        cursor = await self.session.execute(query)
        user_from_db = cursor.all()
        print(user_from_db)
        if not user_from_db:
            raise errors.EntityNotFounded()
        user_from_db = user_from_db[0]
        has_photo = bool(user_from_db[1])
        return UserEntity(
            id=user_from_db.uuid,
            first_name=user_from_db.first_name,
            last_name=user_from_db.last_name,
            patronymic=user_from_db.patronymic,
            phone=user_from_db.phone,
            email=pydantic.EmailStr(user_from_db.email),
            has_access=user_from_db.has_access,
            has_photo=has_photo,
        )

    async def filter(self, page: int = 0) -> ListUserEntity:
        query = select(models.User, models.Photo.id)
        query = query.limit(self.limit).offset((page + 1) * self.limit)
        cursor = await self.session.execute(query)
        return ListUserEntity(
            max_page=1,
            total=1,
            items=[
                UserEntity(
                    id=user_from_db[0].uuid,
                    first_name=user_from_db[0].first_name,
                    last_name=user_from_db[0].last_name,
                    patronymic=user_from_db[0].patronymic,
                    phone=user_from_db[0].phone,
                    email=pydantic.EmailStr(user_from_db[0].email),
                    has_access=user_from_db[0].has_access,
                    has_photo=bool(user_from_db[1]),
                )
                for user_from_db in cursor.all()
            ]
        )
