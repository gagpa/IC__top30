from datetime import timedelta
from uuid import UUID

from fastapi import APIRouter, Depends, Response, status

import domain
from . import (
    dependencies,
    responses,
)

router = APIRouter(prefix='/god_mode')


@router.patch(
    '/admin/{id}',
    status_code=201,
)
async def _get_admin(
        id: UUID,
        add_admin_in_repo__case: domain.admin.use_cases.add.AddAdminInRepo = Depends(dependencies.get__add_admin),
        delete_coach_from_repo: domain.coach.use_cases.delete.DeleteCoachFromRepo =
        Depends(dependencies.get__delete_coach_from_repo),
        delete_student_from_repo: domain.student.use_cases.delete.DeleteStudentFromRepo =
        Depends(dependencies.get__delete_student_from_repo),
):
    await delete_coach_from_repo.delete(user_id=id)
    await delete_student_from_repo.delete(user_id=id)
    await add_admin_in_repo__case.add(user_id=id)


@router.patch(
    '/event/{_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
async def _move_event(
        _id: UUID,
        offset: int,
        move_event__case: domain.event.use_cases.move_event.MoveEventAsGod =
        Depends(dependencies.get__move_event_case),
        find_event_in_repo__case: domain.event.use_cases.find.FindEventInRepo =
        Depends(dependencies.get__find_event_in_repo),
):
    event = await find_event_in_repo__case.find(_id)
    new_start_date = event.start_date + timedelta(hours=int(offset))
    await move_event__case.move(
        event_id=_id,
        new_start_date=new_start_date.replace(minute=0, second=0, microsecond=0),
    )
