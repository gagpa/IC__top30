import fastapi
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.base.client_requests import Client, Role
from api_v1.base.dependencies import get__session, get__client
from domain import student, user


async def get_find_student_in_repo(session: AsyncSession = fastapi.Depends(get__session)):
    student_repo = student.resources.repo.PostgresStudentRepo(session)
    return student.use_cases.find.FindStudentInRepo(student_repo=student_repo)


async def get_find_user_in_repo(session: AsyncSession = fastapi.Depends(get__session)):
    user_repo = user.resources.repo.PostgresUserRepo(session)
    return user.use_cases.find.FindUserInRepo(user_repo=user_repo)


async def get_filter_students_from_repo(limit: int = 20, session: AsyncSession = fastapi.Depends(get__session)):
    student_repo = student.resources.repo.PostgresStudentRepo(session, limit=limit)
    return student.use_cases.filter.FilterStudentsFromRepo(student_repo=student_repo)


async def get__delete_user_from_repo(session: AsyncSession = fastapi.Depends(get__session)):
    user_deleter = user.resources.deleter.PostgresUserDeleter(session=session)
    return user.use_cases.delete.DeleteUserFromRepo(user_deleter=user_deleter)


async def get__delete_student_from_repo(session: AsyncSession = fastapi.Depends(get__session)):
    student_deleter = student.resources.deleter.PostgresStudentDeleter(session=session)
    return student.use_cases.delete.DeleteStudentFromRepo(student_deleter=student_deleter)


async def only__admin(client: Client = fastapi.Depends(get__client)):
    if client.role != Role.ADMIN:
        raise fastapi.HTTPException(403, detail='Нет доступа')


async def only__admin_coach(client: Client = fastapi.Depends(get__client)):
    if client.role not in (Role.ADMIN, Role.COACH):
        raise fastapi.HTTPException(403, detail='Нет доступа')
