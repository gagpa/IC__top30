import uuid

from fastapi import APIRouter, status, Response, Depends

import domain
from . import (

    client_requests,
    dependencies,
    responses,
)

router = APIRouter(
    prefix='/registration_requests',
    dependencies=[Depends(dependencies.only__admin)],
    tags=['Заявки'],
)


@router.patch(
    '/{_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    # response_class=Response,
)
async def _accept(
        _id: uuid.UUID,
        accept_coach_case: domain.coach.use_cases.accept.AcceptCoachInRepo =
        Depends(dependencies.get__accept_coach_in_repo),
):
    await accept_coach_case.accept(coach_id=_id)


@router.get(
    '',
    status_code=status.HTTP_200_OK,
    response_model=responses.ListCoachesStudentsResponse,
)
async def _list(
        filter_coaches_case: domain.coach.use_cases.filter.FilterFreeCoaches =
        Depends(dependencies.get__filter_requests_coaches),
        filter_students_case: domain.student.use_cases.filter.FilterStudents =
        Depends(dependencies.get__filter_requests_students),
        find_user__case: domain.user.use_cases.find.FindUserInRepo = Depends(dependencies.get_find_user_in_repo),
):
    coaches = await filter_coaches_case.filter()
    students = await filter_students_case.filter()
    all_requests = coaches.items + students.items
    users = [await find_user__case.find(coach.user_id) for coach in coaches.items]
    data = responses.UserCoachStudentList(
        max_page=coaches.max_page,
        total=coaches.total,
        items=[
            responses.UserCoach(
                id=data.user_id,
                profession_direction=data.profession_direction,
                specialization=data.specialization,
                experience=data.experience,
                profession_competencies=data.profession_competencies,
                total_seats=data.total_seats,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                phone=user.phone,
                photo=user.photo,
                patronymic=user.patronymic,
                students_ids=[],
            ) if isinstance(data, domain.coach.entity.CoachEntity) else
            responses.UserStudent(
                id=user.id,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
                phone=user.phone,
                position=data.position,
                organization=data.organization,
                experience=data.experience,
                supervisor=data.supervisor,
                patronymic=user.patronymic,
            )
            for user, data in zip(users, all_requests)
        ],
    )

    return responses.ListCoachesStudentsResponse(data=data)
