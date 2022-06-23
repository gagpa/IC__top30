from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import errors
from db.postgres import models
from domain.auth.entity import Role
from .base import AuthorizationService

__all__ = ['PostgresAuthorizationService']


class PostgresAuthorizationService(AuthorizationService):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def auth(self, user_id: UUID) -> Role:
        student_query = select(models.Student).join(models.User).where(models.User.uuid == user_id)
        cursor = await self.session.execute(student_query)
        if cursor.one_or_none():
            return Role.STUDENT
        coach_query = select(models.Coach).join(models.User).where(models.User.uuid == user_id)
        cursor = await self.session.execute(coach_query)
        if cursor.one_or_none():
            return Role.COACH
        admin_query = select(models.Admin).join(models.User).where(models.User.uuid == user_id)
        cursor = await self.session.execute(admin_query)
        if cursor.one_or_none():
            return Role.ADMIN
        raise errors.EntityNotFounded()
