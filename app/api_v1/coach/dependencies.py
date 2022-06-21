import fastapi
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.base.dependencies import get__session, get__client
from api_v1.base.client_requests import Client, Role
from domain import coach, user


async def get_find_coach_in_repo(session: AsyncSession = fastapi.Depends(get__session)):
    coach_repo = coach.resources.repo.PostgresCoachRepo(session)
    return coach.use_cases.find.FindCoachInRepo(coach_repo=coach_repo)


async def get_find_user_in_repo(session: AsyncSession = fastapi.Depends(get__session)):
    user_repo = user.resources.repo.PostgresUserRepo(session)
    return user.use_cases.find.FindUserInRepo(user_repo=user_repo)


async def get_filter_coaches_from_repo(limit: int = 20, session: AsyncSession = fastapi.Depends(get__session)):
    coach_repo = coach.resources.repo.PostgresCoachRepo(session, limit=limit)
    return coach.use_cases.filter.FilterCoachsFromRepo(coach_repo=coach_repo)


async def get__delete_user_from_repo(session: AsyncSession = fastapi.Depends(get__session)):
    user_deleter = user.resources.deleter.PostgresUserDeleter(session=session)
    return user.use_cases.delete.DeleteUserFromRepo(user_deleter=user_deleter)


async def get__delete_coach_from_repo(session: AsyncSession = fastapi.Depends(get__session)):
    coach_deleter = coach.resources.deleter.PostgresCoachDeleter(session=session)
    return coach.use_cases.delete.DeleteCoachFromRepo(coach_deleter=coach_deleter)


async def only__admin(client: Client = fastapi.Depends(get__client)):
    if client.role != Role.ADMIN:
        raise fastapi.HTTPException(403, detail='Нет доступа')


async def only__admin_student(client: Client = fastapi.Depends(get__client)):
    if client.role not in (Role.ADMIN, Role.STUDENT):
        raise fastapi.HTTPException(403, detail='Нет доступа')
