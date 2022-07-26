from datetime import datetime, timedelta
from uuid import UUID

from fastapi import APIRouter, Depends

import domain
from api_v1.base.client_requests import Client
from api_v1.base.dependencies import get__client
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
    status_code=204,
)
async def _move_event(
        _id: UUID,
        offset: int,
        client: Client = Depends(get__client),
        move_event__case: domain.event.use_cases.move_event.MoveEventAsGod =
        Depends(dependencies.get__move_event_case),
        find_user__case: domain.user.use_cases.find.FindUserInRepo = Depends(dependencies.get__find_user_in_repo),
):
    new_start_date = datetime.now() - timedelta(hours=int(offset))
    event = await move_event__case.move(
        student_id=client.user_id,
        event_id=_id,
        new_start_date=new_start_date,
    )
    coach = await find_user__case.find(event.coach)
    student = await find_user__case.find(event.student)
    return responses.FindEventResponse(
        data=responses.Event(
            id=event.id,
            start=int(round(event.start_date.timestamp())) * 1000,
            end=int(round(event.end_date.timestamp())) * 1000,
            student=responses.Student(
                id=event.student,
                first_name=student.first_name,
                last_name=student.last_name,
                patronymic=student.patronymic,
            ),
            coach=responses.Coach(
                id=event.coach,
                first_name=coach.first_name,
                last_name=coach.last_name,
                patronymic=coach.patronymic,
            ),
            status=event.status,
        ),
    )
