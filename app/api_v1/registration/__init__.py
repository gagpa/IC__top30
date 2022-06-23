import typing

from fastapi import APIRouter, Depends

import domain
from . import (
    client_requests,
    dependencies,
    responses,
)

router = APIRouter(tags=['Регистрация'])


@router.post(
    '/sign_up',
    status_code=201
)
async def _sign_up(
        new_user_request: typing.Union[client_requests.SignUpAsStudentRequest, client_requests.SignUpAsCoachRequest],
        add_new_user_case: domain.user.use_cases.add.AddUserInRepo = Depends(dependencies.get__add_user),
        add_new_coach_case: domain.coach.use_cases.add.AddCoachInRepo = Depends(dependencies.get__add_coach),
        add_new_student_case: domain.student.use_cases.add.AddStudentInRepo = Depends(dependencies.get__add_student),
):
    new_user = await add_new_user_case.add(
        password=new_user_request.password,
        first_name=new_user_request.first_name,
        last_name=new_user_request.last_name,
        patronymic=new_user_request.patronymic,
        email=new_user_request.email,
        phone=new_user_request.phone,
        photo=new_user_request.photo,
    )
    if isinstance(new_user_request, client_requests.SignUpAsCoachRequest):
        await add_new_coach_case.add(
            user_id=new_user.id,
            profession_direction=new_user_request.profession_direction,
            specialization=new_user_request.specialization,
            experience=new_user_request.experience,
            profession_competencies=new_user_request.profession_competencies,
            total_seats=new_user_request.total_seats,
        )
    elif isinstance(new_user_request, client_requests.SignUpAsStudentRequest):
        await add_new_student_case.add(
            user_id=new_user.id,
            position=new_user_request.position,
            organization=new_user_request.organization,
            experience=new_user_request.experience,
            supervisor=new_user_request.supervisor,
        )
