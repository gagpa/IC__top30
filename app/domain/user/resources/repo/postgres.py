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
        print(password, first_name, last_name, patronymic, phone, email, photo)
        new_user = models.User(
            password=password,
            first_name=first_name,
            last_name=last_name,
            patronymic=patronymic,
            phone=phone,
            email=email,
            photo=photo,
        )
        self.session.add(new_user)
        await self.session.flush()
        return UserEntity(
            id=new_user.uuid,
            first_name=new_user.first_name,
            last_name=new_user.last_name,
            patronymic=new_user.patronymic,
            phone=new_user.phone,
            email=pydantic.EmailStr(new_user.email),
            photo=new_user.photo,
            has_access=new_user.has_access,
        )

    async def find(self, id: UUID) -> UserEntity:
        query = select(models.User).where(models.User.uuid == id)
        cursor = await self.session.execute(query)
        user_from_db = cursor.one_or_none()[0]
        if not user_from_db:
            raise errors.EntityNotFounded()
        return UserEntity(
            id=user_from_db.uuid,
            first_name=user_from_db.first_name,
            last_name=user_from_db.last_name,
            patronymic=user_from_db.patronymic,
            phone=user_from_db.phone,
            email=pydantic.EmailStr(user_from_db.email),
            photo=user_from_db.photo,
            has_access=user_from_db.has_access,
        )

    async def filter(self, page: int = 0) -> ListUserEntity:
        query = select(models.User)
        query = query.limit(self.limit).offset((page + 1) * self.limit)
        cursor = await self.session.execute(query)
        return ListUserEntity(
            max_page=1,
            total=1,
            items=[
                UserEntity(
                    id=user_from_db.uuid,
                    first_name=user_from_db.first_name,
                    last_name=user_from_db.last_name,
                    patronymic=user_from_db.patronymic,
                    phone=user_from_db.phone,
                    email=pydantic.EmailStr(user_from_db.email),
                    photo=user_from_db.photo,
                    has_access=user_from_db.has_access,
                )
                for user_from_db in cursor.scalars()
            ]
        )
