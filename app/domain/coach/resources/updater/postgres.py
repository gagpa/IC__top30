import typing
from uuid import UUID

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres import models
from .base import CoachUpdater


class PostgresCoachUpdater(CoachUpdater):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def update(
            self,
            coach_id: UUID,
            has_access: typing.Optional[bool] = None,
            first_name: typing.Optional[str] = None,
            last_name: typing.Optional[str] = None,
            patronymic: typing.Optional[str] = None,
            phone: typing.Optional[str] = None,
            photo: typing.Optional[str] = None,
            profession_direction: typing.Optional[str] = None,
            specialization: typing.Optional[str] = None,
            experience: typing.Optional[str] = None,
            profession_competencies: typing.Optional[str] = None,
            total_seats: typing.Optional[int] = None,
    ):
        query = update(models.User).where(models.User.uuid == coach_id)

        if isinstance(has_access, bool):
            query.values(has_access=has_access)
        if first_name:
            query = query.values(first_name=first_name)
        if last_name:
            query = query.values(last_name=last_name)
        if patronymic:
            query = query.values(patronymic=patronymic)
        if phone:
            query = query.values(phone=phone)
        if photo:
            query = query.values(photo=photo)
        if profession_competencies:
            query = query.values(profession_competencies=profession_competencies)
        if specialization:
            query = query.values(specialization=specialization)
        if experience:
            query = query.values(experience=experience)
        if profession_competencies:
            query = query.values(profession_competencies=profession_competencies)
        if total_seats:
            query = query.values(total_seats=total_seats)

        await self.session.execute(query)
