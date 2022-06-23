import typing
from uuid import UUID

from sqlalchemy import select, func
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
            self,
            user_id: UUID,
            total_seats: int,
            profession_direction: str,
            specialization: str,
            experience: str,
            profession_competencies: str,
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
            total_seats=total_seats,
            profession_direction=profession_direction,
            specialization=specialization,
            experience=experience,
            profession_competencies=profession_competencies,
        )
        self.session.add(new_coach)
        return CoachEntity(
            user_id=user_id,
            profession_direction=profession_direction,
            specialization=specialization,
            experience=experience,
            profession_competencies=profession_competencies,
            total_seats=total_seats,
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
            profession_direction=coach_from_db.profession_direction,
            specialization=coach_from_db.specialization,
            experience=coach_from_db.experience,
            profession_competencies=coach_from_db.profession_competencies,
            total_seats=coach_from_db.total_seats
        )

    async def filter(self, is_free: typing.Optional[bool] = None, page: int = 0) -> ListCoachEntity:
        query = select(models.Coach)

        # if isinstance(is_free, bool):
        #     subquery = select(models.Coach.id, func(models.User).count()).join(models.Coach).group_by(models.Coach.id)
        #     if is_free:
        #         subquery = subquery.having(student_count < models.Coach.total_seats).subquery()
        #     else:
        #         subquery = subquery.having(student_count < models.Coach.total_seats).subquery()
        #     query = query.where(models.Coach.id.in_(subquery.id))

        query = query.limit(self.limit).offset((page + 1) * self.limit)
        cursor = await self.session.execute(query)
        return ListCoachEntity(
            total=1,
            max_page=1,
            items=[
                CoachEntity(
                    user_id=coach_from_db.user_data.uuid,
                    profession_direction=coach_from_db.profession_direction,
                    specialization=coach_from_db.specialization,
                    experience=coach_from_db.experience,
                    profession_competencies=coach_from_db.profession_competencies,
                    total_seats=coach_from_db.total_seats
                )
                for coach_from_db in cursor.scalars()
            ]
        )