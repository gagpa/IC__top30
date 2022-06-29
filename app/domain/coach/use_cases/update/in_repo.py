import typing
from uuid import UUID

from domain.coach.resources.updater import CoachUpdater
from .base import UpdateCoach


class UpdateCoachInRepo(UpdateCoach):

    def __init__(self, coach_updater: CoachUpdater):
        self.coach_updater = coach_updater

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
        await self.coach_updater.update(
            coach_id=coach_id,
            has_access=has_access,
            first_name=first_name,
            last_name=last_name,
            patronymic=patronymic,
            phone=phone,
            photo=photo,
            profession_competencies=profession_competencies,
            profession_direction=profession_direction,
            specialization=specialization,
            experience=experience,
            total_seats=total_seats,
        )
