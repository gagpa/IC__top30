import uuid

from fastapi import APIRouter, Depends, status, Response

import domain
from . import (
    dependencies,
    responses,
)

router = APIRouter(
    prefix='/user',
    tags=['Личный профиль'],
)


# @router.get('/{user_id}/avatar')
# async def _avatar(user_id: UUID, get_user_photo_case: Depends(get__get_user_photo)):
#     get_user_photo_case.get_photo(user_id)
#     return


@router.patch(
    '/{id}',
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    dependencies=[Depends(dependencies.only__admin)]
)
async def _accept(
        _id: uuid.UUID,
        accept_student_case: domain.student.use_cases.accept.AcceptStudentInRepo =
        Depends(dependencies.get__accept_student_in_repo),
        accept_coach_case: domain.coach.use_cases.accept.AcceptCoachInRepo =
        Depends(dependencies.get__accept_coach_in_repo),
):
    await accept_student_case.accept(student_id=_id)
    await accept_coach_case.accept(coach_id=_id)
