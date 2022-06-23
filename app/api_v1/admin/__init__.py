from uuid import UUID

from fastapi import APIRouter, Depends

import domain
from . import dependencies

router = APIRouter(prefix='/god_mode')


@router.patch(
    '/admin/{id}',
    status_code=201,
)
async def _get_admin(
        id: UUID,
        add_admin_in_repo__case: domain.admin.use_cases.add.AddAdminInRepo = Depends(dependencies.get__add_admin),
        delete_coach_from_repo: domain.coach.use_cases.delete.DeleteCoachFromRepo =
        Depends(dependencies.get__delete_coach_from_repo),
        delete_student_from_repo: domain.student.use_cases.delete.DeleteStudentFromRepo =
        Depends(dependencies.get__delete_student_from_repo),
):
    await delete_coach_from_repo.delete(user_id=id)
    await delete_student_from_repo.delete(user_id=id)
    await add_admin_in_repo__case.add(user_id=id)
