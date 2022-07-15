import typing
from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, Response, status

import domain
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
        client: Client = Depends(get__client),
        filter_events__case: typing.Union[
            domain.event.use_cases.filter.FilterEventsForStudent,
            domain.event.use_cases.filter.FilterEventsForCoach,
        ] = Depends(dependencies.get__filter_events__case)
):
    events = await filter_events__case.filter(client.user_id)
    return responses.FilterEventResponse(
        data=responses.EventList(
            max_page=events.max_page,
            total=events.total,
            items=[
                responses.Event(
                    id=event.id,
                    start_date=int(round(event.start_date.timestamp())) * 1000,
                    end_date=int(round(event.end_date.timestamp())) * 1000,
                    student_id=event.student,
                )
                for event in events.items
            ],
        )
    )


@router.post(
    '',
    dependencies=[Depends(dependencies.only__student)],
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
async def _add(
        new_event: client_requests.NewEventRequest,
        client: Client = Depends(get__client),
        add_event__case: domain.event.use_cases.add.AddEventAsStudent = Depends(dependencies.get__add_event_case)
):
    await add_event__case.add(
        start_date=datetime.fromtimestamp(int(new_event.start) / 1000),
        end_date=datetime.fromtimestamp(int(new_event.end) / 1000),
        student_id=client.user_id,
    )


@router.put(
    '/{_id}',
    dependencies=[Depends(dependencies.only__coach_student)],
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
async def _move(
        _id: UUID,
        new_start_date: int,
        client: Client = Depends(get__client),
        move_event__case: domain.event.use_cases.move_event.MoveEventAsStudent =
        Depends(dependencies.get__move_event_case)
):
    await move_event__case.move(
        student_id=client.user_id,
        event_id=_id,
        new_start_date=datetime.fromtimestamp(int(new_start_date) / 1000),
    )
