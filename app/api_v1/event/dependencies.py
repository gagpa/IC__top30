import fastapi
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.base.client_requests import Client
from api_v1.base.dependencies import get__client, get__session
from domain import auth, event, slot


async def only__coach_student(client: Client = fastapi.Depends(get__client)):
    if client.role not in (auth.entity.Role.COACH, auth.entity.Role.STUDENT):
        raise fastapi.HTTPException(403, detail='Нет доступа')


async def only__student(client: Client = fastapi.Depends(get__client)):
    if client.role != auth.entity.Role.STUDENT:
        raise fastapi.HTTPException(403, detail='Нет доступа')


async def get__filter_events__case(
        client: Client = fastapi.Depends(get__client),
        session: AsyncSession = fastapi.Depends(get__session),
):
    if client.role == auth.entity.Role.COACH:
        event_repo = event.resources.repo.PostgresEventRepo(session=session)
        return event.use_cases.filter.FilterEventsForCoach(event_repo=event_repo)
    elif client.role == auth.entity.Role.STUDENT:
        event_repo = event.resources.repo.PostgresEventRepo(session=session)
        return event.use_cases.filter.FilterEventsForStudent(event_repo=event_repo)
    raise Exception


async def get__add_event_case(session: AsyncSession = fastapi.Depends(get__session)):
    event_repo = event.resources.repo.PostgresEventRepo(session=session)
    slot_repo = slot.resources.repo.PostrgesSlotRepo(session=session)
    return event.use_cases.add.AddEventAsStudent(event_repo=event_repo, slot_repo=slot_repo)


async def get__move_event_case(session: AsyncSession = fastapi.Depends(get__session)):
    event_repo = event.resources.repo.PostgresEventRepo(session=session)
    event_mover = event.resources.mover.PostgresEventMover(session=session)
    return event.use_cases.move_event.MoveEventAsStudent(event_mover=event_mover, event_repo=event_repo)
