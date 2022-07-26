import fastapi
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.base.dependencies import get__session
from domain import admin, coach, student, event, user


async def get__delete_coach_from_repo(session: AsyncSession = fastapi.Depends(get__session)):
    coach_deleter = coach.resources.deleter.PostgresCoachDeleter(session=session)
    return coach.use_cases.delete.DeleteCoachFromRepo(coach_deleter=coach_deleter)


async def get__delete_student_from_repo(session: AsyncSession = fastapi.Depends(get__session)):
    student_deleter = student.resources.deleter.PostgresStudentDeleter(session=session)
    return student.use_cases.delete.DeleteStudentFromRepo(student_deleter=student_deleter)


async def get__add_admin(session: AsyncSession = fastapi.Depends(get__session)):
    admin_repo = admin.resources.repo.PostgresAdminRepo(session=session)
    return admin.use_cases.add.AddAdminInRepo(admin_repo=admin_repo)


async def get__move_event_case(session: AsyncSession = fastapi.Depends(get__session)):
    event_repo = event.resources.repo.PostgresEventRepo(session=session)
    event_mover = event.resources.mover.PostgresEventMover(session=session)
    return event.use_cases.move_event.MoveEventAsGod(event_mover=event_mover, event_repo=event_repo)


async def get__find_user_in_repo(session: AsyncSession = fastapi.Depends(get__session)):
    user_repo = user.resources.repo.PostgresUserRepo(session)
    return user.use_cases.find.FindUserInRepo(user_repo=user_repo)
