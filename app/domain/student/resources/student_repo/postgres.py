import typing
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

import errors
from db.postgres import models
from domain.student.entity import StudentEntity, ListStudentEntity
from .base import StudentRepo


class PostgresStudentRepo(StudentRepo):

    def __init__(self, session: AsyncSession, limit: int = 20):
        self.session = session
        self.limit = limit

    async def add(
            self, user_id: UUID, position: str, organization: str, experience: str, supervisor: str,
    ) -> StudentEntity:
        query = select(models.Student).join(models.User).where(models.User.uuid == user_id)
        cursor = await self.session.execute(query)
        if cursor.one_or_none():
            raise errors.EntityAlreadyExist
        query_user = select(models.User).where(models.User.uuid == user_id)
        cursor = await self.session.execute(query_user)
        user = cursor.one()[0]
        new_student = models.Student(
            user_id=user.id,
            position=position,
            organization=organization,
            experience=experience,
            supervisor=supervisor,
        )
        self.session.add(new_student)
        return StudentEntity(
            user_id=user_id,
            position=position,
            organization=organization,
            experience=experience,
            supervisor=supervisor,
        )

    async def find(self, user_id: UUID) -> StudentEntity:
        query = select(models.Student).join(models.User).where(models.User.uuid == user_id)
        cursor = await self.session.execute(query)
        try:
            student_from_db: typing.Optional[models.Student] = cursor.one()
            student_from_db = student_from_db[0]
            if student_from_db.coach_id:
                query = select(models.User.uuid).join(models.Coach).where(models.Coach.id == student_from_db.coach_id)
                cursor = await self.session.execute(query)
                coach_id = cursor.one()[0]
            else:
                coach_id = None
        except NoResultFound:
            raise errors.EntityNotFounded()
        return StudentEntity(
            user_id=user_id,
            position=student_from_db.position,
            organization=student_from_db.organization,
            experience=student_from_db.experience,
            supervisor=student_from_db.supervisor,
            coach_id=coach_id,
        )

    async def filter(
            self,
            has_access: bool = True,
            coach_id: typing.Optional[UUID] = None,
            page: int = 0,
    ) -> ListStudentEntity:
        query = select(models.Student). \
            join(models.User). \
            options(joinedload(models.Student.user_data))
        if coach_id:
            subquery = select(models.Coach.id).join(models.User).where(models.User.uuid == coach_id).subquery()
            query = query.where(models.Student.coach_id == subquery)
        query = query.where(models.User.has_access == has_access)
        query = query.limit(self.limit).offset(page * self.limit)
        cursor = await self.session.execute(query.where(models.User.is_deleted == False))
        students = [student[0] for student in cursor.all()]
        coaches_ids = [student.coach_id for student in students if student.coach_id]
        coaches_query = select(models.Coach.id, models.User.uuid).join(models.Coach).where(
            models.Coach.id.in_(coaches_ids))
        coaches_cursor = await self.session.execute(coaches_query)
        coaches_uuids = {coach_id: user_id for coach_id, user_id in coaches_cursor.all()}
        return ListStudentEntity(
            total=1,
            max_page=1,
            items=[
                StudentEntity(
                    user_id=student_from_db.user_data.uuid,
                    position=student_from_db.position,
                    organization=student_from_db.organization,
                    experience=student_from_db.experience,
                    supervisor=student_from_db.supervisor,
                    coach_id=coaches_uuids.get(student_from_db.coach_id),
                )
                for student_from_db in students
            ]
        )
