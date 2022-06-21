import uuid

from fastapi import APIRouter, Depends, status, Response

import domain
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
            profession=coach.profession,
            specialization=coach.specialization,
            experience=coach.experience,
            key_specializations=coach.key_specializations,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            phone=user.phone,
            photo=user.photo,
        )
    )


@router.get(
    '',
    response_model=responses.ListCoachesResponse,
)
async def _filter(
        page: int = 0,
        filter_coaches_case: domain.coach.use_cases.filter.FilterCoachsFromRepo =
        Depends(dependencies.get_filter_coaches_from_repo),
        find_user_case: domain.user.use_cases.find.FindUserInRepo = Depends(dependencies.get_find_user_in_repo),
):
    coaches = await filter_coaches_case.filter(page=page)
    users = [await find_user_case.find(coach.user_id) for coach in coaches.items]
    return responses.ListCoachesResponse(
        data=responses.UserCoachList(
            max_page=coaches.max_page,
            total=coaches.total,
            items=[
                responses.UserCoach(
                    id=user.id,
                    email=user.email,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    phone=user.phone,
                    photo=user.photo,
                    profession=coach.profession,
                    specialization=coach.specialization,
                    experience=coach.experience,
                    key_specializations=coach.key_specializations,
                )
                for user, coach in zip(users, coaches)
            ],
        )
    )


@router.delete(
    '/{id}',
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
async def _delete(
        id: uuid.UUID,
        delete_coach_case: domain.coach.use_cases.delete.DeleteCoachFromRepo =
        Depends(dependencies.get__delete_coach_from_repo),
        delete_user_case: domain.user.use_cases.delete.DeleteUserFromRepo =
        Depends(dependencies.get__delete_user_from_repo),
):
    await delete_coach_case.delete(user_id=id)
    await delete_user_case.delete(id=id)
