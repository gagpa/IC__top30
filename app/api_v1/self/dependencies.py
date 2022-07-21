import fastapi
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.base.client_requests import Client
from api_v1.base.dependencies import get__session, get__client
from domain import admin, coach, user, auth, student


async def get__find_coach_in_repo(session: AsyncSession = fastapi.Depends(get__session)):
    coach_repo = coach.resources.repo.PostgresCoachRepo(session)
    return coach.use_cases.find.FindCoachInRepo(coach_repo=coach_repo)


async def get__find_user_in_repo(session: AsyncSession = fastapi.Depends(get__session)):
    user_repo = user.resources.repo.PostgresUserRepo(session)
    return user.use_cases.find.FindUserInRepo(user_repo=user_repo)


async def get__find_student_in_repo(session: AsyncSession = fastapi.Depends(get__session)):
    student_repo = student.resources.student_repo.PostgresStudentRepo(session)
    return student.use_cases.find.FindStudentInRepo(student_repo=student_repo)


async def get__update_student_in_repo(session: AsyncSession = fastapi.Depends(get__session)):
    student_updater = student.resources.updater.PostgresStudentUpdater(session)
    student_repo = student.resources.student_repo.PostgresStudentRepo(session)
    return student.use_cases.update.UpdateStudentInRepo(student_updater=student_updater, student_repo=student_repo)


async def get__update_coach_in_repo(session: AsyncSession = fastapi.Depends(get__session)):
    coach_updater = coach.resources.updater.PostgresCoachUpdater(session)
    return coach.use_cases.update.UpdateCoachInRepo(coach_updater=coach_updater)


async def get__update_admin_in_repo(session: AsyncSession = fastapi.Depends(get__session)):
    admin_updater = admin.resources.updater.PostgresAdminUpdater(session)
    return admin.use_cases.update.UpdateAdminInRepo(admin_updater=admin_updater)


async def only__student(client: Client = fastapi.Depends(get__client)):
    if client.role != auth.entity.Role.STUDENT:
        raise fastapi.HTTPException(403, detail='Нет доступа')


async def get__refuse_a_personal_coach(session: AsyncSession = fastapi.Depends(get__session)):
    student_repo = student.resources.student_repo.PostgresStudentRepo(session=session)
    coach_changer = student.resources.personal_coach_changer.PostgresPersonalCoachChanger(session=session)
    return student.use_cases.refuse_personal_coach.SoftRefusePersonalCoach(
        student_repo=student_repo,
        coach_changer=coach_changer,
    )


async def get__choose_free_coach(session: AsyncSession = fastapi.Depends(get__session)):
    personal_coach_changer = student.resources.personal_coach_changer.PostgresPersonalCoachChanger(session=session)
    coach_verifier = student.resources.coach_verifier.PostrgesCoachVerifier(session=session)
    return student.use_cases.choose_coach.ChooseCoachFree(
        personal_coach_changer=personal_coach_changer,
        coach_verifier=coach_verifier,
    )
