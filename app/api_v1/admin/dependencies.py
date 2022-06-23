import fastapi
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.base.dependencies import get__session
from domain import admin, coach, student


async def get__delete_coach_from_repo(session: AsyncSession = fastapi.Depends(get__session)):
    coach_deleter = coach.resources.deleter.PostgresCoachDeleter(session=session)
    return coach.use_cases.delete.DeleteCoachFromRepo(coach_deleter=coach_deleter)


async def get__delete_student_from_repo(session: AsyncSession = fastapi.Depends(get__session)):
    student_deleter = student.resources.deleter.PostgresStudentDeleter(session=session)
    return student.use_cases.delete.DeleteStudentFromRepo(student_deleter=student_deleter)


async def get__add_admin(session: AsyncSession = fastapi.Depends(get__session)):
    admin_repo = admin.resources.repo.PostgresAdminRepo(session=session)
    return admin.use_cases.add.AddAdminInRepo(admin_repo=admin_repo)
