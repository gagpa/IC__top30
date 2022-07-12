import typing
from uuid import UUID

import sqlalchemy as sql
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.util._collections import immutabledict

from db.postgres import models
from domain.student.entity import StudentEntity
from .base import PersonalCoachChanger


class PostgresPersonalCoachChanger(PersonalCoachChanger):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def change(self, student: UUID, new_coach: typing.Optional[UUID]) -> StudentEntity:
        subquery_user = sql.select(models.User.id).where(models.User.uuid == student).subquery()
        query = sql.update(models.Student).where(models.Student.user_id == subquery_user)
        subquery_new_coach = sql.select(models.Coach.id).join(models.User).where(
            models.User.uuid == new_coach).subquery()
        cursor = await self.session.execute(
            query.values(coach_id=subquery_new_coach),
            execution_options=immutabledict({'synchronize_session': 'fetch'}),
        )
        # student_from_db = cursor.one()[0]
        # return StudentEntity(
        #     user_id=student,
        #     position=student_from_db.position,
        #     organization=student_from_db.organization,
        #     experience=student_from_db.experience,
        #     supervisor=student_from_db.supervisor,
        #     coach_id=new_coach,
        # )
