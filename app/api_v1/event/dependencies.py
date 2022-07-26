import fastapi
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.base.client_requests import Client
from api_v1.base.dependencies import get__client, get__session
from domain import auth, event, slot, coach, user, student


async def only__coach_student(client: Client = fastapi.Depends(get__client)):
    if client.role not in (auth.entity.Role.COACH, auth.entity.Role.STUDENT):
        raise fastapi.HTTPException(403, detail='Нет доступа')


async def only__student(client: Client = fastapi.Depends(get__client)):
    if client.role != auth.entity.Role.STUDENT:
        raise fastapi.HTTPException(403, detail='Нет доступа')


async def only__coach_student_admin(client: Client = fastapi.Depends(get__client)):
    if client.role not in (auth.entity.Role.COACH, auth.entity.Role.STUDENT, auth.entity.Role.ADMIN):
        raise fastapi.HTTPException(403, detail='Нет доступа')


async def get__filter_events__case(
        client: Client = fastapi.Depends(get__client),
        session: AsyncSession = fastapi.Depends(get__session),
):
    if client.role in (auth.entity.Role.COACH, auth.entity.Role.ADMIN):
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


async def get__cancel_event_case(
        client: Client = fastapi.Depends(get__client),
        session: AsyncSession = fastapi.Depends(get__session),
):
    event_deleter = event.resources.deleter.PostgrestEventDeleter(session=session)
    event_repo = event.resources.repo.PostgresEventRepo(session=session)

    if client.role == auth.entity.Role.STUDENT:
        event_status_changer = event.resources.stutus_changer.PostgresEventStatusChanger(session=session)
        return event.use_cases.cancel.CancelEventAsStudent(
            event_deleter=event_deleter,
            event_repo=event_repo,
            event_status_changer=event_status_changer,
        )
    elif client.role == auth.entity.Role.COACH:
        return event.use_cases.cancel.CancelEventAsCoach(
            event_deleter=event_deleter,
            event_repo=event_repo,
        )
    raise Exception


async def get__find_coach_in_repo(session: AsyncSession = fastapi.Depends(get__session)):
    coach_repo = coach.resources.repo.PostgresCoachRepo(session)
    return coach.use_cases.find.FindCoachInRepo(coach_repo=coach_repo)


async def get__find_user_in_repo(session: AsyncSession = fastapi.Depends(get__session)):
    user_repo = user.resources.repo.PostgresUserRepo(session)
    return user.use_cases.find.FindUserInRepo(user_repo=user_repo)


async def get__find_student_in_repo(session: AsyncSession = fastapi.Depends(get__session)):
    student_repo = student.resources.student_repo.PostgresStudentRepo(session)
    return student.use_cases.find.FindStudentInRepo(student_repo=student_repo)


async def get__find_event_in_repo(session: AsyncSession = fastapi.Depends(get__session)):
    event_repo = event.resources.repo.PostgresEventRepo(session)
    return event.use_cases.find.FindEventInRepo(event_repo=event_repo)
