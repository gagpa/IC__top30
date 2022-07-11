import fastapi
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.base.client_requests import Client
from api_v1.base.dependencies import get__session, get__client
from domain import auth, slot
from domain.auth.entity import Role


async def get__filter_slots(
        client: Client = fastapi.Depends(get__client),
        session: AsyncSession = fastapi.Depends(get__session),
):
    slot_repo = slot.resources.repo.PostrgesSlotRepo(session=session)
    if client.role == Role.COACH:
        return slot.use_cases.filter_slots.FilterSlotsForCoach(slot_repo=slot_repo)
    elif client.role == Role.STUDENT:
        return slot.use_cases.filter_slots.FilterSlotsForStudent(slot_repo=slot_repo)
    raise Exception


async def only__coach_student(
        client: Client = fastapi.Depends(get__client),
):
    if client.role not in (auth.entity.Role.COACH, auth.entity.Role.STUDENT):
        raise fastapi.HTTPException(403, detail='Нет доступа')


async def only__coach(
        client: Client = fastapi.Depends(get__client),
):
    if client.role != auth.entity.Role.COACH:
        raise fastapi.HTTPException(403, detail='Нет доступа')


async def get__delete_slot(session: AsyncSession = fastapi.Depends(get__session)):
    slot_deleter = slot.resources.deleter.PostgresSlotDeleter(session=session)
    return slot.use_cases.delete.DeleteSlotFromRepo(slot_deleter=slot_deleter)


async def get__add_slots(session: AsyncSession = fastapi.Depends(get__session)):
    slot_repo = slot.resources.repo.PostrgesSlotRepo(session=session)
    return slot.use_cases.add.AddSlotInRepo(slot_repo=slot_repo)
