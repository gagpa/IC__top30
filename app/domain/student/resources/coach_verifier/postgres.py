from uuid import UUID

import sqlalchemy as sql
from sqlalchemy.ext.asyncio import AsyncSession

import errors
from db.postgres import models
from .base import CoachVerifier


class PostrgesCoachVerifier(CoachVerifier):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def is_free(self, coach_id: UUID):
        subquery_coach = sql.select(models.Coach.id).join(models.User).where(models.User.uuid == coach_id).subquery()
        subquery_count_of_students = sql.select(sql.func.count(models.Student.id)).where(models.Student.coach_id == subquery_coach).subquery()
        query = sql.select(models.Coach).where(
            models.Coach.id == subquery_coach,
            models.Coach.total_seats > subquery_count_of_students,
        )
        cursor = await self.session.execute(query)
        if not cursor.one_or_none():
            raise errors.EntityNotFounded()
