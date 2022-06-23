import fastapi
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.base.dependencies import get__session
from domain import coach, user, student


async def get__find_coach_in_repo(session: AsyncSession = fastapi.Depends(get__session)):
    coach_repo = coach.resources.repo.PostgresCoachRepo(session)
    return coach.use_cases.find.FindCoachInRepo(coach_repo=coach_repo)


async def get__find_user_in_repo(session: AsyncSession = fastapi.Depends(get__session)):
    user_repo = user.resources.repo.PostgresUserRepo(session)
    return user.use_cases.find.FindUserInRepo(user_repo=user_repo)


async def get__find_student_in_repo(session: AsyncSession = fastapi.Depends(get__session)):
    student_repo = student.resources.repo.PostgresStudentRepo(session)
    return student.use_cases.find.FindStudentInRepo(student_repo=student_repo)
