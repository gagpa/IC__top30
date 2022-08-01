from datetime import datetime
from uuid import UUID

import sqlalchemy as sql
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

import errors
from db.postgres import models
from domain.event.entity import EventEntity
from .base import EventMover


class PostgresEventMover(EventMover):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def move(self, event_id: UUID, new_start_date: datetime) -> EventEntity:
        event_size = await self.__select__event_size(event_id)
        new_slots_for_event = await self.__select__new_slots_for_event(event_id, new_start_date, event_size)
        if len(new_slots_for_event) < event_size:
            raise errors.EntityAlreadyExist()
        try:
            event = await self.__select__event(event_id)
        except NoResultFound:
            raise errors.EntityNotFounded()
        event.slots = new_slots_for_event
        start_date = self.__calculate__start_date(new_slots_for_event)
        end_date = self.__calculate__end_date(new_slots_for_event)
        event.start_date = start_date
        event.end_date = end_date
        self.session.add(event)

        return EventEntity(
            id=event.uuid,
            status=event.status,
            coach=await self.__select__coach_id(new_slots_for_event[0]),
            student=await self.__select__student_id(event),
            start_date=start_date,
            end_date=end_date,
        )

    async def __select__event_size(self, event_id: UUID) -> int:
        query = sql.select(sql.func.count(models.Slot.id)). \
            join(models.pivot__slots_events, models.pivot__slots_events.c.slot_id == models.Slot.id). \
            join(models.Event, models.Event.id == models.pivot__slots_events.c.event_id). \
            where(models.Event.uuid == event_id)
        cursor = await self.session.execute(query)
        return cursor.scalar()

    async def __select__new_slots_for_event(
            self, event_id: UUID, new_start_date: datetime, event_size: int,
    ):
        query = sql.select(models.Slot).where(
            models.Slot.coach_id == (
                sql.select(models.Student.coach_id).join(models.Event).where(models.Event.uuid == event_id).subquery()
            ),
            models.Slot.start_date >= new_start_date,
        ).order_by(models.Slot.start_date).limit(event_size)
        cursor = await self.session.execute(query)
        result = cursor.all()
        return [row[0] for row in result]

    async def __select__event(self, event_id: UUID):
        query = sql.select(models.Event). \
            where(models.Event.uuid == event_id). \
            options(selectinload(models.Event.slots))
        cursor = await self.session.execute(query)
        return cursor.one()[0]

    async def __select__coach_id(self, slot) -> UUID:
        cursor = await self.session.execute(
            sql.select(models.User.uuid).join(models.Coach).where(models.Coach.id == slot.coach_id)
        )
        return cursor.scalar()

    async def __select__student_id(self, event) -> UUID:
        cursor = await self.session.execute(
            sql.select(models.User.uuid).join(models.Student).where(models.Student.id == event.student_id)
        )
        return cursor.scalar()

    def __calculate__start_date(self, slots: list) -> datetime:
        return min([slot.start_date for slot in slots])

    def __calculate__end_date(self, slots: list) -> datetime:
        return max([slot.end_date for slot in slots])
