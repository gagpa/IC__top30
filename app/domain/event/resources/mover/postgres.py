from datetime import datetime
from uuid import UUID

import sqlalchemy as sql
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
        query__slots = sql.select(models.Slot). \
            join(models.pivot__slots_events, models.pivot__slots_events.c.slot_id == models.Slot.id). \
            join(models.Event, models.Event.id == models.pivot__slots_events.c.event_id). \
            where(models.Event.uuid == event_id)
        cursor = await self.session.execute(query__slots)
        slots = cursor.all()
        print(slots)
        event_size = len(slots)
        subquery__coach_id = sql.select(models.Student.coach_id). \
            join(models.Event). \
            where(models.Event.uuid == event_id). \
            subquery()
        subquery__coach = sql.select(models.Coach.id).where(models.Coach.id == subquery__coach_id).subquery()
        query__possible_slots = sql.select(models.Slot).where(
            models.Slot.coach_id == subquery__coach,
            models.Slot.start_date >= new_start_date,
        ).order_by(models.Slot.start_date)
        cursor = await self.session.execute(query__possible_slots)
        possible_slots = cursor.all()
        if len(possible_slots) < event_size:
            raise errors.EntityAlreadyExist
        print(possible_slots)
        print(event_size)
        new_slots_for_event = [slot[0] for slot in possible_slots[:event_size]]
        print(new_slots_for_event)
        cursor = await self.session.execute(
            sql.select(models.Event).where(models.Event.uuid == event_id).options(selectinload(models.Event.slots))
        )
        event = cursor.one()[0]
        event.slots = new_slots_for_event
        self.session.add(event)
        start = min([slot.start_date for slot in new_slots_for_event])
        end = max([slot.end_date for slot in new_slots_for_event])
        coach = await self.session.execute(
            sql.select(models.User.uuid).join(models.Coach).where(models.Coach.id == new_slots_for_event[0].coach_id)
        )
        student = await self.session.execute(
            sql.select(models.User.uuid).join(models.Student).where(models.Student.id == event.student_id)
        )
        return EventEntity(
            id=event.uuid,
            status=event.status,
            coach=coach.one()[0],
            student=student.one()[0],
            start_date=start,
            end_date=end,
        )
