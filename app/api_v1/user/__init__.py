from fastapi import APIRouter, Depends

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
            photo=user.photo,
            patronymic=user.patronymic,
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
            photo=user.photo,
            patronymic=user.patronymic,
        )
    else:
        admin = await find_user__case.find(client.user_id)
        data = responses.SelfAdmin(
            id=client.user_id,
            first_name=admin.first_name,
            last_name=admin.last_name,
            email=admin.email,
            phone=admin.phone,
            photo=admin.photo,
            patronymic=admin.patronymic,
        )
    return responses.SelfResponse(data=data)
