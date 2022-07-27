import uuid

import fastapi
from fastapi import APIRouter, Depends, status, Response

import domain
from api_v1.base.client_requests import Client
from domain.auth.entity import Role  # TODO : архитектурная ошибка
from . import (
    client_requests,
    dependencies,
    responses,
)

router = APIRouter(
    prefix='/coaches',
    tags=['Наставник'],
    dependencies=[Depends(dependencies.only__admin_student)],
)


@router.get(
    '/{id}',
    response_model=responses.CoachByIDResponse,
    dependencies=[Depends(dependencies.only__admin_student)],
)
async def _find(
        id: uuid.UUID,
        find_coach_case: domain.coach.use_cases.find.FindCoachInRepo = Depends(dependencies.get_find_coach_in_repo),
        find_user_case: domain.user.use_cases.find.FindUserInRepo = Depends(dependencies.get_find_user_in_repo),
):
    coach = await find_coach_case.find(user_id=id)
    user = await find_user_case.find(id=id)
    return responses.CoachByIDResponse(
        data=responses.UserCoach(
            id=id,
            profession_direction=coach.profession_direction,
            specialization=coach.specialization,
            experience=coach.experience,
            profession_competencies=coach.profession_competencies,
            total_seats=coach.total_seats,
            students_ids=coach.students,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            phone=user.phone,
            patronymic=user.patronymic,
            photo=f'https://top30mt.ru/api/v1/user/{coach.user_id}/avatar',
        )
    )


@router.get(
    '',
    response_model=responses.ListCoachesResponse,
    dependencies=[Depends(dependencies.only__admin_student)],
)
async def _filter(
        page: int = 0,
        client: Client = Depends(dependencies.get__client),
        filter_coaches__case: domain.coach.use_cases.filter.FilterAllCoaches =
        Depends(dependencies.get__filter_all_coaches),
        filter_free_coaches__case: domain.coach.use_cases.filter.FilterFreeCoaches =
        Depends(dependencies.get__filter_free_coaches),
        find_user__case: domain.user.use_cases.find.FindUserInRepo = Depends(dependencies.get_find_user_in_repo),
):
    if client.role == Role.ADMIN:
        coaches = await filter_coaches__case.filter(page=page)
    elif client.role == Role.STUDENT:
        client = await find_user__case.find(client.user_id)  # TODO: Пересмотреть этот момент
        if client.coach_id:
            raise fastapi.HTTPException(403, detail='Нет доступа')
        coaches = await filter_free_coaches__case.filter(page=page)
    else:
        raise fastapi.HTTPException(403, detail='Нет доступа')

    users = [await find_user__case.find(coach.user_id) for coach in coaches.items]
    return responses.ListCoachesResponse(
        data=responses.UserCoachList(
            max_page=coaches.max_page,
            total=coaches.total,
            items=[
                responses.UserCoach(
                    id=coach.user_id,
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
                    photo=f'https://top30mt.ru/api/v1/user/{coach.user_id}/avatar',
                )
                for user, coach in zip(users, coaches.items)
            ],
        )
    )


@router.delete(
    '/{_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    dependencies=[Depends(dependencies.only__admin)]
)
async def _delete(
        _id: uuid.UUID,
        delete_coach_case: domain.coach.use_cases.delete.DeleteCoachFromRepo =
        Depends(dependencies.get__delete_coach_from_repo),
        delete_user_case: domain.user.use_cases.delete.DeleteUserFromRepo =
        Depends(dependencies.get__delete_user_from_repo),
):
    await delete_coach_case.delete(user_id=_id)
    await delete_user_case.delete(id=_id)
