from uuid import UUID

import sqlalchemy as sql
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres import models
from .base import StudentService


class PostgresStudentService(StudentService):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_coach(self, student_id: UUID, coach_id: UUID):
        query = sql.update(models.Student).join(models.User).where(models.User.uuid == student_id)
        subquery_coach = sql.select(models.Coach.id).join(models.User).where(models.User.uuid == coach_id)
        query = query.values(coach_id=subquery_coach)
        await self.session.execute(query)

    async def decline_coach(self, student_id: UUID):
        query = sql.update(models.Student).join(models.User).where(models.User.uuid == student_id)
        query = query.values(coach_id=None)
        await self.session.execute(query)
