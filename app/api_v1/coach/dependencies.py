import fastapi
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.base.client_requests import Client
from api_v1.base.dependencies import get__session, get__client
from domain import coach, user, auth, student, event


async def get_find_coach_in_repo(session: AsyncSession = fastapi.Depends(get__session)):
    coach_repo = coach.resources.repo.PostgresCoachRepo(session)
    return coach.use_cases.find.FindCoachInRepo(coach_repo=coach_repo)


async def get_find_user_in_repo(session: AsyncSession = fastapi.Depends(get__session)):
    user_repo = user.resources.repo.PostgresUserRepo(session)
    return user.use_cases.find.FindUserInRepo(user_repo=user_repo)


async def get__filter_all_coaches(limit: int = 20, session: AsyncSession = fastapi.Depends(get__session)):
    coach_repo = coach.resources.repo.PostgresCoachRepo(session, limit=limit)
    return coach.use_cases.filter.FilterAllCoaches(coach_repo=coach_repo)


async def get__filter_free_coaches(limit: int = 20, session: AsyncSession = fastapi.Depends(get__session)):
    coach_repo = coach.resources.repo.PostgresCoachRepo(session, limit=limit)
    return coach.use_cases.filter.FilterFreeCoaches(coach_repo=coach_repo)


async def get__delete_user_from_repo(session: AsyncSession = fastapi.Depends(get__session)):
    user_deleter = user.resources.deleter.PostgresUserDeleter(session=session)
    return user.use_cases.delete.DeleteUserFromRepo(user_deleter=user_deleter)


async def get__delete_coach_from_repo(session: AsyncSession = fastapi.Depends(get__session)):
    coach_deleter = coach.resources.deleter.PostgresCoachDeleter(session=session)
    coach_repo = coach.resources.repo.PostgresCoachRepo(session=session)
    coach_changer = student.resources.personal_coach_changer.PostgresPersonalCoachChanger(session=session)
    event_status_changer = event.resources.stutus_changer.PostgresEventStatusChanger(session=session)
    event_repo = event.resources.repo.PostgresEventRepo(session=session)
    event_deleter = event.resources.deleter.PostgrestEventDeleter(session=session)
    return coach.use_cases.delete.DeleteCoachFromRepo(
        coach_deleter=coach_deleter,
        event_status_changer=event_status_changer,
        event_repo=event_repo,
        event_deleter=event_deleter,
        coach_repo=coach_repo,
        coach_changer=coach_changer,
    )


async def only__admin(client: Client = fastapi.Depends(get__client)):
    if client.role != auth.entity.Role.ADMIN:
        raise fastapi.HTTPException(403, detail='Нет доступа')


async def only__student(client: Client = fastapi.Depends(get__client)):
    if client.role != auth.entity.Role.STUDENT:
        raise fastapi.HTTPException(403, detail='Нет доступа')


async def only__admin_student(client: Client = fastapi.Depends(get__client)):
    if client.role not in (auth.entity.Role.ADMIN, auth.entity.Role.STUDENT):
        raise fastapi.HTTPException(403, detail='Нет доступа')


async def get__accept_coach_in_repo(session: AsyncSession = fastapi.Depends(get__session)):
    coach_updater = coach.resources.updater.PostgresCoachUpdater(session=session)
    return coach.use_cases.accept.AcceptCoachInRepo(coach_updater=coach_updater)


async def get__choose_free_coach(session: AsyncSession = fastapi.Depends(get__session)):
    student_service = student.resources.service.PostgresStudentService(session=session)
    coach_verifier = student.resources.coach_verifier.PostrgesCoachVerifier(session=session)
    return student.use_cases.choose_coach.ChooseCoachFree(
        coach_verifier=coach_verifier,
        student_service=student_service,
    )
