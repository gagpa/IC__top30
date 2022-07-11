import typing
from datetime import datetime, timedelta
from uuid import UUID

from fastapi import APIRouter, Depends, status, Query
from fastapi.responses import Response

import domain
from api_v1.base.client_requests import Client
from api_v1.base.dependencies import get__client
from . import (
    client_requests,
    dependencies,
    responses,
)

router = APIRouter(tags=['Слоты'], prefix='/slots')


@router.get(
    '',
    response_model=responses.FilterSlotResponse,
    status_code=200,
    dependencies=[Depends(dependencies.only__coach_student)],
)
async def _filter(
        client: Client = Depends(get__client),
        page: int = 0,
        filter_slots__case: typing.Union[
            domain.slot.use_cases.filter_slots.FilterSlotsForCoach,
            domain.slot.use_cases.filter_slots.FilterSlotsForStudent,
        ] = Depends(dependencies.get__filter_slots),
):
    slots = await filter_slots__case.filter(client.user_id, page=page)
    return responses.FilterSlotResponse(
        data=responses.SlotList(
            max_page=slots.max_page,
            total=slots.total,
            items=[
                responses.Slot(
                    id=slot.id,
                    start_date=slot.start_date,
                    end_date=slot.end_date,
                )
                for slot in slots.items
            ],
        )
    )


@router.delete(
    '/{_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    dependencies=[Depends(dependencies.only__coach_student)],
)
async def _delete(
        _id: UUID,
        dates: typing.List[int] = Query(...),
        delete_slot__case: domain.slot.use_cases.delete.DeleteSlotFromRepo = Depends(dependencies.get__delete_slot),
):
    await delete_slot__case.delete(dates=[datetime.fromtimestamp(date) for date in dates])


@router.post(
    '',
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(dependencies.only__coach)]
)
async def _add(
        client: Client = Depends(get__client),
        dates: typing.List[int] = Query(...),
        add_slots__case: domain.slot.use_cases.add.AddSlotInRepo = Depends(dependencies.get__add_slots),
):
    delta_hour = timedelta(hours=1)
    for date in dates:
        start_date = datetime.fromtimestamp(date)
        await add_slots__case.add(coach_id=client.user_id, start_date=start_date, end_date=start_date + delta_hour)
