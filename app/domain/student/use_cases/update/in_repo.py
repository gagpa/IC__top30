import typing
from uuid import UUID

from domain.student.resources.updater import StudentUpdater
from .base import UpdateStudent


class UpdateStudentInRepo(UpdateStudent):

    def __init__(self, student_updater: StudentUpdater):
        self.student_updater = student_updater

    async def update(
            self,
            student_id: UUID,
            has_access: typing.Optional[bool] = None,
            first_name: typing.Optional[str] = None,
            last_name: typing.Optional[str] = None,
            patronymic: typing.Optional[str] = None,
            phone: typing.Optional[str] = None,
            position: typing.Optional[str] = None,
            photo: typing.Optional[str] = None,
            experience: typing.Optional[str] = None,
            supervisor: typing.Optional[str] = None,
    ):
        await self.student_updater.update(
            student_id=student_id,
            has_access=has_access,
            first_name=first_name,
            last_name=last_name,
            patronymic=patronymic,
            phone=phone,
            position=position,
            photo=photo,
            experience=experience,
            supervisor=supervisor,
        )
