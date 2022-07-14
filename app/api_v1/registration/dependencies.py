from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.base.dependencies import get__session, get__secret_key
from domain import coach, user, student, auth


async def get__add_user(session: AsyncSession = Depends(get__session), secret_key: str = Depends(get__secret_key)):
    return user.use_cases.add.AddUserInRepo(
        user_repo=user.resources.repo.PostgresUserRepo(session=session),
        password_hasher=auth.resources.password_hasher.BcryptPasswordHasher(secret_key=secret_key),
    )


async def get__add_coach(session: AsyncSession = Depends(get__session)):
    return coach.use_cases.add.AddCoachInRepo(coach_repo=coach.resources.repo.PostgresCoachRepo(session=session))


async def get__add_student(session: AsyncSession = Depends(get__session)):
    return student.use_cases.add.AddStudentInRepo(
        student_repo=student.resources.student_repo.PostgresStudentRepo(session=session),
    )
