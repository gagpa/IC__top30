import typing
from datetime import datetime
from uuid import UUID

import sqlalchemy as sql
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, aliased
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
        subquery__slots_ids = sql.select(models.Slot.id).where(
            models.Slot.start_date.between(start_date, end_date),
            models.Slot.end_date.between(start_date, end_date),
        ).subquery()
        check_exist_query = sql.select(models.Event).join(models.pivot__slots_events).where(
            models.Event.student_id == subquery__student_id,
            models.pivot__slots_events.c.slot_id.in_(subquery__slots_ids),
        )
        cursor = await self.session.execute(check_exist_query)
        if cursor.one_or_none():
            raise errors.EntityAlreadyExist
        query__slots = sql.select(models.Slot).where(
            models.Slot.start_date.between(start_date, end_date),
            models.Slot.end_date.between(start_date, end_date),
        )
        cursor = await self.session.execute(query__slots)
        slots = [slot[0] for slot in cursor.all()]
        new_event = models.Event(slots=slots, student_id=subquery__student_id, status=EventStatus.active)
        self.session.add(new_event)

    async def find(self, event_id: UUID) -> EventEntity:
        coach_user__alias = aliased(models.User)
        student_user__alias = aliased(models.User)
        query = sql.select(models.Event, student_user__alias.uuid, coach_user__alias.uuid). \
            join(models.Student, models.Event.student_id == models.Student.id). \
            join(student_user__alias, student_user__alias.id == models.Student.user_id). \
            join(models.Coach, models.Coach.id == models.Student.coach_id). \
            join(coach_user__alias, coach_user__alias.id == models.Coach.user_id). \
            options(selectinload(models.Event.slots))
        cursor = await self.session.execute(query)
        try:
            data = cursor.one()
            event_from_db: models.Event = data[0]
            student_id: UUID = data[1]
            coach_id: UUID = data[2]
        except NoResultFound:
            raise errors.EntityNotFounded
        return EventEntity(
            id=event_from_db.uuid,
            status=event_from_db.status,
            coach=coach_id,
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
        coach_user__alias = aliased(models.User)
        student_user__alias = aliased(models.User)
        query = sql.select(models.Event, student_user__alias.uuid, coach_user__alias.uuid). \
            join(models.Student, models.Event.student_id == models.Student.id). \
            join(student_user__alias, student_user__alias.id == models.Student.user_id). \
            join(models.Coach, models.Coach.id == models.Student.coach_id). \
            join(coach_user__alias, coach_user__alias.id == models.Coach.user_id). \
            options(selectinload(models.Event.slots))
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
                    id=data[0].uuid,
                    status=data[0].status,
                    student=data[1],
                    coach=data[2],
                    start_date=min([slot.start_date for slot in data[0].slots]),
                    end_date=max([slot.end_date for slot in data[0].slots]),
                )
                for data in cursor.all()
            ],
        )
