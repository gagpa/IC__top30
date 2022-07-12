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
        subquery_count_of_students = sql.select(sql.func.count(models.Student.id)).where(coach_id=coach_id).subquery()
        query = sql.select(models.Coach).where(
            coach_id == coach_id,
            models.Coach.total_seats > subquery_count_of_students,
        )
        cursor = await self.session.execute(query)
        if not cursor.one_or_none():
            raise errors.EntityNotFounded()
