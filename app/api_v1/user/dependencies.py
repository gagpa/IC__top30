import fastapi
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.base.client_requests import Client
from api_v1.base.dependencies import get__session, get__client
from domain import coach, auth, student


async def only__admin(client: Client = fastapi.Depends(get__client)):
    if client.role != auth.entity.Role.ADMIN:
        raise fastapi.HTTPException(403, detail='Нет доступа')


async def get__accept_coach_in_repo(session: AsyncSession = fastapi.Depends(get__session)):
    coach_updater = coach.resources.updater.PostgresCoachUpdater(session=session)
    return coach.use_cases.accept.AcceptCoachInRepo(coach_updater=coach_updater)


async def get__accept_student_in_repo(session: AsyncSession = fastapi.Depends(get__session)):
    student_updater = student.resources.updater.PostgresStudentUpdater(session=session)
    return student.use_cases.accept.AcceptStudentInRepo(student_updater=student_updater)
