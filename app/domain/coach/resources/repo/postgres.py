import typing
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

import errors
from db.postgres import models
from domain.coach.entity import CoachEntity, ListCoachEntity
from .base import CoachRepo


class PostgresCoachRepo(CoachRepo):

    def __init__(self, session: AsyncSession, limit: int = 20):
        self.session = session
        self.limit = limit

    async def add(
            self, user_id: UUID, profession: str, specialization: str, experience: str, key_specializations: str
    ) -> CoachEntity:
        query = select(models.Coach).join(models.User).where(models.User.uuid == user_id)
        cursor = await self.session.execute(query)
        if cursor.one_or_none():
            raise errors.EntityAlreadyExist
        query_user = select(models.User).where(models.User.uuid == user_id)
        cursor = await self.session.execute(query_user)
        user = cursor.one()
        new_coach = models.Coach(
            user_id=user.id,
            profession=profession,
            specialization=specialization,
            experience=experience,
            key_specializations=key_specializations,
        )
        self.session.add(new_coach)
        return CoachEntity(
            user_id=user_id,
            profession=profession,
            specialization=specialization,
            experience=experience,
            key_specializations=key_specializations,
        )

    async def find(self, user_id: UUID) -> CoachEntity:
        query = select(models.Coach).join(models.User).where(models.User.uuid == user_id)
        cursor = await self.session.execute(query)
        try:
            coach_from_db: typing.Optional[models.Coach] = cursor.one()
        except NoResultFound:
            raise errors.EntityNotFounded()
        return CoachEntity(
            user_id=user_id,
            profession=coach_from_db.profession,
            specialization=coach_from_db.specialization,
            experience=coach_from_db.experience,
            key_specializations=coach_from_db.key_specializations,
        )

    async def filter(self, page: int = 0) -> ListCoachEntity:
        query = select(models.Coach)
        query = query.limit(self.limit).offset((page + 1) * self.limit)
        cursor = await self.session.execute(query)
        return ListCoachEntity(
            total=1,
            max_page=1,
            items=[
                CoachEntity(
                    user_id=coach_from_db.user_data.uuid,
                    profession=coach_from_db.profession,
                    specialization=coach_from_db.specialization,
                    experience=coach_from_db.experience,
                    key_specializations=coach_from_db.key_specializations,
                )
                for coach_from_db in cursor.scalars()
            ]
        )
