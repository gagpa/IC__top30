import fastapi
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.base.dependencies import get__session
from domain import admin, coach, student, event, user, slot


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


async def get__delete_student_from_repo(session: AsyncSession = fastapi.Depends(get__session)):
    student_deleter = student.resources.deleter.PostgresStudentDeleter(session=session)
    event_deleter = event.resources.deleter.PostgrestEventDeleter(session=session)
    event_repo = event.resources.repo.PostgresEventRepo(session=session)
    return student.use_cases.delete.DeleteStudentFromRepo(
        student_deleter=student_deleter,
        event_deleter=event_deleter,
        event_repo=event_repo,
    )


async def get__add_admin(session: AsyncSession = fastapi.Depends(get__session)):
    admin_repo = admin.resources.repo.PostgresAdminRepo(session=session)
    return admin.use_cases.add.AddAdminInRepo(admin_repo=admin_repo)


async def get__move_event_case(session: AsyncSession = fastapi.Depends(get__session)):
    event_repo = event.resources.repo.PostgresEventRepo(session=session)
    event_mover = event.resources.mover.PostgresEventMover(session=session)
    student_repo = student.resources.student_repo.PostgresStudentRepo(session=session)
    slot_repo = slot.resources.repo.PostrgesSlotRepo(session=session)
    return event.use_cases.move_event.MoveEventAsGod(
        event_mover=event_mover,
        event_repo=event_repo,
        student_repo=student_repo,
        slot_repo=slot_repo,
    )


async def get__find_user_in_repo(session: AsyncSession = fastapi.Depends(get__session)):
    user_repo = user.resources.repo.PostgresUserRepo(session)
    return user.use_cases.find.FindUserInRepo(user_repo=user_repo)


async def get__find_event_in_repo(session: AsyncSession = fastapi.Depends(get__session)):
    event_repo = event.resources.repo.PostgresEventRepo(session)
    return event.use_cases.find.FindEventInRepo(event_repo=event_repo)
