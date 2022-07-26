import typing
from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, status

import domain
import errors
from api_v1.base.client_requests import Client
from api_v1.base.dependencies import get__client
from . import (
    client_requests,
    dependencies,
    responses,
)

router = APIRouter(tags=['События'], prefix='/event')


@router.get(
    '',
    dependencies=[Depends(dependencies.only__coach_student)],
    response_model=responses.FilterEventResponse,
)
async def _filter(
        student_id: typing.Optional[UUID] = None,
        client: Client = Depends(get__client),
        filter_events__case: typing.Union[
            domain.event.use_cases.filter.FilterEventsForStudent,
            domain.event.use_cases.filter.FilterEventsForCoach,
        ] = Depends(dependencies.get__filter_events__case),
        find_user__case: domain.user.use_cases.find.FindUserInRepo = Depends(dependencies.get__find_user_in_repo),
):
    events = await filter_events__case.filter(client.user_id, student_id=student_id)
    items = []
    for event in events.items:
        coach = await find_user__case.find(event.coach)
        student = await find_user__case.find(event.student)
        items.append(
            responses.Event(
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
            )
        )
    return responses.FilterEventResponse(
        data=responses.EventList(
            max_page=events.max_page,
            total=events.total,
            items=items,
        )
    )


@router.post(
    '',
    dependencies=[Depends(dependencies.only__student)],
    status_code=status.HTTP_201_CREATED,
    response_model=responses.FindEventResponse,
)
async def _add(
        new_event: client_requests.NewEventRequest,
        client: Client = Depends(get__client),
        add_event__case: domain.event.use_cases.add.AddEventAsStudent = Depends(dependencies.get__add_event_case),
        find_user__case: domain.user.use_cases.find.FindUserInRepo = Depends(dependencies.get__find_user_in_repo),
):
    event = await add_event__case.add(
        start_date=datetime.fromtimestamp(int(new_event.start) / 1000),
        end_date=datetime.fromtimestamp(int(new_event.end) / 1000),
        student_id=client.user_id,
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


@router.put(
    '/{_id}',
    dependencies=[Depends(dependencies.only__coach_student)],
    status_code=status.HTTP_200_OK,
    response_model=responses.FindEventResponse,
)
async def _move(
        _id: UUID,
        new_start_date: int,
        client: Client = Depends(get__client),
        move_event__case: domain.event.use_cases.move_event.MoveEventAsStudent =
        Depends(dependencies.get__move_event_case),
        find_user__case: domain.user.use_cases.find.FindUserInRepo = Depends(dependencies.get__find_user_in_repo),
):
    event = await move_event__case.move(
        student_id=client.user_id,
        event_id=_id,
        new_start_date=datetime.fromtimestamp(int(new_start_date) / 1000),
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


@router.delete(
    '/{_id}',
    dependencies=[Depends(dependencies.only__coach_student)],
    status_code=status.HTTP_200_OK,
    response_model=responses.FindEventResponse,
)
async def _cancel(
        _id: UUID,
        cancel_event__case: typing.Union[
            domain.event.use_cases.cancel.CancelEventAsStudent,
            domain.event.use_cases.cancel.CancelEventAsCoach,
        ] = Depends(dependencies.get__cancel_event_case),
        find_event__case: domain.event.use_cases.find.FindEventInRepo = Depends(dependencies.get__find_event_in_repo),
        find_user__case: domain.user.use_cases.find.FindUserInRepo = Depends(dependencies.get__find_user_in_repo),
):
    event = await find_event__case.find(event_id=_id)
    await cancel_event__case.cancel(event_id=_id)
    try:
        event = await find_event__case.find(event_id=_id)
    except errors.EntityNotFounded:
        pass
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
