import typing
from datetime import datetime
from uuid import UUID

import sqlalchemy as sql
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

import errors
from db.postgres import models
from .base import EventMover


class PostgresEventMover(EventMover):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def move(self, event_id: UUID, new_start_date: datetime):
        query__slots = sql.select(models.Slot). \
            join(models.pivot__slots_events, models.pivot__slots_events.c.slot_id == models.Slot.id). \
            join(models.Event, models.Event.id == models.pivot__slots_events.c.event_id). \
            where(models.Event.uuid == event_id)
        cursor = await self.session.execute(query__slots)
        slots: typing.List[models.Slot] = cursor.all()[0]
        start = min([slot.start_date for slot in slots])
        end = max([slot.end_date for slot in slots])
        time_delta = end - start
        subquery__coach_id = sql.select(models.Student.coach_id). \
            join(models.Event). \
            where(models.Event.uuid == event_id). \
            subquery()
        subquery__coach = sql.select(models.Coach.id).where(models.Coach.id == subquery__coach_id).subquery()
        query__possible_slots = sql.select(models.Slot).where(
            models.Slot.coach_id == subquery__coach,
            models.Slot.start_date >= new_start_date,
        )
        cursor = await self.session.execute(query__possible_slots)
        possible_slots = cursor.all()
        if len(possible_slots) < len(slots):
            raise errors.EntityAlreadyExist
        new_slots_for_event = possible_slots[:len(slots)]
        cursor = await self.session.execute(
            sql.select(models.pivot__slots_events).where(models.Event.uuid == event_id)
        )
        event_slot_links = cursor.all()
        for link, new_slot in zip(event_slot_links, new_slots_for_event):
            print(link)
            print(new_slot)
            link[0].c.slot_id = new_slot.id
            self.session.add(link[0])
