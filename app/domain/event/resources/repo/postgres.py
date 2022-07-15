import typing
from datetime import datetime
from uuid import UUID

import sqlalchemy as sql
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

import errors
from db.postgres import models
from domain.event.entity import EventEntity, EventStatus, ListEventEntity
from .base import EventRepo


class PostgresEventRepo(EventRepo):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, start_date: datetime, end_date: datetime, student_id: UUID) -> EventEntity:
        subquery__student_id = sql.select(models.Student.id).join(models.User).where(
            models.User.uuid == student_id).subquery()
        subquery__slots = sql.select(models.Slot.start_date).where(
            models.Slot.start_date.between(start_date, end_date),
            models.Slot.end_date.between(start_date, end_date),
        )
        check_exist_query = sql.select(models.Event).where(
            models.Event.student_id == subquery__student_id,
            models.Event.slots.in_(subquery__slots),
        )
        cursor = await self.session.execute(check_exist_query)
        if cursor.one_or_none():
            raise errors.EntityAlreadyExist
        insert_query = sql.insert(models.Event).values(
            slots=subquery__slots,
            status=EventStatus.active,
            student_id=subquery__student_id,
        )
        await self.session.execute(insert_query)

    async def find(self, event_id: UUID) -> EventEntity:
        query = sql.select(models.Event, models.User.uuid). \
            join(models.Student, models.Event.student_id == models.Student.id). \
            join(models.User, models.User.id == models.Student.user_id). \
            where(models.Event.uuid == event_id)
        cursor = await self.session.execute(query)
        try:
            data = cursor.one()
            event_from_db: models.Event = data[0]
            student_id: UUID = data[1]
        except NoResultFound:
            raise errors.EntityNotFounded
        return EventEntity(
            id=event_from_db.uuid,
            status=event_from_db.status,
            student=student_id,
            start_date=min([slot.start_date for slot in event_from_db.slots]),
            end_date=max([slot.end_date for slot in event_from_db.slots]),
        )

    async def filter(
            self,
            coach_id: typing.Optional[UUID],
            student_id: typing.Optional[UUID],
            page: int = 0,
    ) -> ListEventEntity:
        query = sql.select(models.Event, models.User.uuid). \
            join(models.Student, models.Event.student_id == models.Student.id). \
            join(models.User, models.User.id == models.Student.user_id)
        if coach_id:
            subquery_students_id_of_coach = sql.select(models.Student.id). \
                join(models.Coach, models.Student.coach_id == models.Coach.id). \
                join(models.User, models.User.id == models.Coach.user_id). \
                where(models.User.uuid == coach_id). \
                subquery()
            query = query.where(models.Event.student_id.in_(subquery_students_id_of_coach))
        if student_id:
            query = query.where(models.User.uuid == student_id)
        cursor = await self.session.execute(query)
        return ListEventEntity(
            max_page=1,
            total=1,
            items=[
                EventEntity(
                    id=event_from_db.uuid,
                    status=event_from_db.status,
                    student=foreign__student_id,
                    start_date=min([slot.start_date for slot in event_from_db.slots]),
                    end_date=max([slot.end_date for slot in event_from_db.slots]),
                )
                for event_from_db, foreign__student_id in cursor.all()
            ],
        )