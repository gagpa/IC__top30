import fastapi
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.base.client_requests import Client
from api_v1.base.dependencies import get__session, get__client
from domain import coach, auth, student, user


async def only__admin(client: Client = fastapi.Depends(get__client)):
    if client.role != auth.entity.Role.ADMIN:
        raise fastapi.HTTPException(403, detail='Нет доступа')


async def get__accept_coach_in_repo(session: AsyncSession = fastapi.Depends(get__session)):
    coach_updater = coach.resources.updater.PostgresCoachUpdater(session=session)
    return coach.use_cases.accept.AcceptCoachInRepo(coach_updater=coach_updater)


async def get__accept_student_in_repo(session: AsyncSession = fastapi.Depends(get__session)):
    student_updater = student.resources.updater.PostgresStudentUpdater(session=session)
    return student.use_cases.accept.AcceptStudentInRepo(student_updater=student_updater)


async def get__find_user_photo(session: AsyncSession = fastapi.Depends(get__session)):
    user_repo = user.resources.repo.PostgresUserRepo(session=session)
    return user.use_cases.find_photo.FindLastPhoto(user_repo=user_repo)


async def get__add_photo_to_user(session: AsyncSession = fastapi.Depends(get__session)):
    user_photo_repo = user.resources.user_photo_repo.PostgresUserPhotoRepo(session=session)
    user_repo = user.resources.repo.PostgresUserRepo(session=session)
    return user.use_cases.add_photo.AddPhotoInRepo(user_repo=user_repo, user_photo_repo=user_photo_repo)


async def get__delete_user_photo_from_repo(session: AsyncSession = fastapi.Depends(get__session)):
    user_photo_deleter = user.resources.user_photo_deleter.PostgresUserPhotoDeleter(session=session)
    user_repo = user.resources.repo.PostgresUserRepo(session=session)
    return user.use_cases.delete_user_photo.DeleteUserPhotoFromRepo(
        user_repo=user_repo,
        user_photo_deleter=user_photo_deleter,
    )
