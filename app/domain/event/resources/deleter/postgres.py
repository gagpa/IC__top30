from uuid import UUID

import sqlalchemy as sql
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.util._collections import immutabledict

from db.postgres import models
from .base import EventDeleter


class PostgrestEventDeleter(EventDeleter):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def delete(self, event_id: UUID):
        query = sql.delete(models.Event).where(models.Event.uuid == event_id)
        await self.session.execute(query, execution_options=immutabledict({'synchronize_session': 'fetch'}))
