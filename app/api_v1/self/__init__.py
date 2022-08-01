from fastapi import APIRouter, Depends, Response, status
from uuid import UUID
import domain
from api_v1.base.client_requests import Client
from api_v1.base.dependencies import get__client
from domain.auth.entity import Role  # TODO : архитектурная ошибка
from . import (
    client_requests,
    dependencies,
    responses,
)

router = APIRouter(
    prefix='/self',
    tags=['Личный профиль'],
)


@router.get(
    '',
    response_model=responses.SelfResponse,
)
async def _find(
        client: Client = Depends(get__client),
        find_coach__case: domain.coach.use_cases.find.FindCoachInRepo = Depends(dependencies.get__find_coach_in_repo),
        find_student__case: domain.student.use_cases.find.FindStudentInRepo =
        Depends(dependencies.get__find_student_in_repo),
        find_user__case: domain.user.use_cases.find.FindUserInRepo = Depends(dependencies.get__find_user_in_repo),
):
    if client.role == Role.COACH:
        user = await find_user__case.find(client.user_id)
        coach = await find_coach__case.find(client.user_id)
        data = responses.SelfCoach(
            id=client.user_id,
            profession_direction=coach.profession_direction,
            specialization=coach.specialization,
            experience=coach.experience,
            profession_competencies=coach.profession_competencies,
            total_seats=coach.total_seats,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            phone=user.phone,
            patronymic=user.patronymic,
            students_ids=coach.students,
            photo=f'https://top30mt.ru/api/v1/user/{client.user_id}/avatar' if user.has_photo else None,
        )
    elif client.role == Role.STUDENT:
        user = await find_user__case.find(client.user_id)
        student = await find_student__case.find(client.user_id)
        data = responses.SelfStudent(
            id=client.user_id,
            position=student.position,
            organization=student.organization,
            experience=student.experience,
            supervisor=student.supervisor,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            phone=user.phone,
            patronymic=user.patronymic,
            coach_id=student.coach_id,
            photo=f'https://top30mt.ru/api/v1/user/{client.user_id}/avatar' if user.has_photo else None,
        )
    else:
        user = await find_user__case.find(client.user_id)
        admin = await find_user__case.find(client.user_id)
        data = responses.SelfAdmin(
            id=client.user_id,
            first_name=admin.first_name,
            last_name=admin.last_name,
            email=admin.email,
            phone=admin.phone,
            patronymic=admin.patronymic,
            photo=f'https://top30mt.ru/api/v1/user/{client.user_id}/avatar' if user.has_photo else None,
        )
    return responses.SelfResponse(data=data)


@router.put(
    '',
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
async def _update(
        update_fields: client_requests.UserUpdateFields,
        client: Client = Depends(get__client),
        update_coach_case: domain.coach.use_cases.update.UpdateCoachInRepo =
        Depends(dependencies.get__update_coach_in_repo),
        update_student_case: domain.student.use_cases.update.UpdateStudentInRepo =
        Depends(dependencies.get__update_student_in_repo),
        update_admin_case: domain.admin.use_cases.update.UpdateAdminInRepo =
        Depends(dependencies.get__update_admin_in_repo),
):
    if client.role == Role.COACH:
        await update_coach_case.update(
            coach_id=client.user_id,
            email=update_fields.email,
            first_name=update_fields.first_name,
            last_name=update_fields.last_name,
            patronymic=update_fields.patronymic,
            phone=update_fields.phone,
            photo=update_fields.photo,
            profession_direction=update_fields.profession_direction,
            profession_competencies=update_fields.profession_competencies,
            total_seats=update_fields.total_seats,
        )
    elif client.role == Role.STUDENT:
        await update_student_case.update(
            student_id=client.user_id,
            first_name=update_fields.first_name,
            last_name=update_fields.last_name,
            patronymic=update_fields.patronymic,
            email=update_fields.email,
            phone=update_fields.phone,
            position=update_fields.position,
            photo=update_fields.photo,
            experience=update_fields.experience,
            supervisor=update_fields.supervisor,
            coach_id=update_fields.coach_id,
        )
    else:
        await update_admin_case.update(
            admin_id=client.user_id,
            first_name=update_fields.first_name,
            last_name=update_fields.last_name,
            patronymic=update_fields.patronymic,
            phone=update_fields.phone,
            photo=update_fields.photo,
        )


@router.patch(
    '/personal_coach/{_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    dependencies=[Depends(dependencies.only__student)],
    summary='Выбрать коуча',
)
async def _accept_personal_coach(
        _id: UUID,
        client: Client = Depends(dependencies.get__client),
        choose_free_coach__case: domain.student.use_cases.choose_coach.ChooseCoachFree =
        Depends(dependencies.get__choose_free_coach),
):
    await choose_free_coach__case.choose(student_id=client.user_id, coach_id=_id)


@router.delete(
    '/personal_coach',
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    dependencies=[Depends(dependencies.only__student)],
    summary='Отказаться от коуча',
)
async def _decline_personal_coach(
        client: Client = Depends(dependencies.get__client),
        refuse_a_coach__case: domain.student.use_cases.refuse_personal_coach.SoftRefusePersonalCoach =
        Depends(dependencies.get__refuse_a_personal_coach),
):
    await refuse_a_coach__case.refuse(student_id=client.user_id)


@router.delete(
    '/personal_student/{_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    dependencies=[Depends(dependencies.only__coach)],
)
async def _decline_personal_student(
        _id: UUID,
        refuse_a_student__case: domain.coach.use_cases.refuse_personal_student.SoftRefusePersonalStudent =
        Depends(dependencies.get__refuse_a_personal_student),
):
    await refuse_a_student__case.refuse(student_id=_id)
