from datetime import datetime
from uuid import UUID

import sqlalchemy as sql
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres import models
from .base import EventMover


class PostgresEventMover(EventMover):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def move(self, event_id: UUID, new_start_date: datetime):
        subquery__slots = sql.select(models.Slot).join(models.Event).where(models.Event.uuid == event_id)
        query = sql.update(models.Event).where(models.Event.uuid == event_id).values(slots=subquery__slots)
        await self.session.execute(query)
