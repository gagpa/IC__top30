from uuid import UUID

import sqlalchemy as sql
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.util._collections import immutabledict

from db.postgres import models
from .base import SlotCleaner


class PostgresSlotCleaner(SlotCleaner):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def clean(self, event_id: UUID):
        event_id__subquery = sql.select(models.Event.id).where(models.Event.uuid == event_id).subquery()
        query = sql.delete(models.pivot__slots_events). \
            where(models.pivot__slots_events.c.event_id == event_id__subquery)
        await self.session.execute(query, execution_options=immutabledict({'synchronize_session': 'fetch'}))
