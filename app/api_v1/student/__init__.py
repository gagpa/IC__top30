import typing
import uuid

from fastapi import APIRouter, Depends, status, Response

import domain
from . import (
    client_requests,
    dependencies,
    responses,
)

router = APIRouter(
    prefix='/students',
    tags=['Студент'],
    dependencies=[Depends(dependencies.only__admin_coach)],
)


@router.get(
    '/{id}',
    response_model=responses.StudentByIDResponse,
)
async def _find(
        id: uuid.UUID,
        find_student_case: domain.student.use_cases.find.FindStudentInRepo = Depends(
            dependencies.get_find_student_in_repo),
        find_user_case: domain.user.use_cases.find.FindUserInRepo = Depends(dependencies.get_find_user_in_repo),
):
    student = await find_student_case.find(user_id=id)
    user = await find_user_case.find(id=id)
    return responses.StudentByIDResponse(
        data=responses.UserStudent(
            id=id,
            position=student.position,
            organization=student.organization,
            experience=student.experience,
            supervisor=student.supervisor,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            phone=user.phone,
            patronymic=user.patronymic,
            has_access=user.has_access,
            photo=f'https://top30mt.ru/api/v1/user/{student.user_id}/avatar' if user.has_photo else None,
        )
    )


@router.get(
    '',
    response_model=responses.ListstudentsResponse,
)
async def _filter(
        page: int = 0,
        coach_id: typing.Optional[uuid.UUID] = None,
        filter_students_case: domain.student.use_cases.filter.FilterStudentsFromRepo =
        Depends(dependencies.get_filter_students_from_repo),
        find_user_case: domain.user.use_cases.find.FindUserInRepo = Depends(dependencies.get_find_user_in_repo),
):
    students = await filter_students_case.filter(coach_id=coach_id, page=page)
    users = [await find_user_case.find(student.user_id) for student in students.items]
    return responses.ListstudentsResponse(
        data=responses.UserStudentList(
            max_page=students.max_page,
            total=students.total,
            items=[
                responses.UserStudent(
                    id=user.id,
                    email=user.email,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    phone=user.phone,
                    position=student.position,
                    organization=student.organization,
                    experience=student.experience,
                    supervisor=student.supervisor,
                    patronymic=user.patronymic,
                    has_access=user.has_access,
                    coach_id=student.coach_id,
                    photo=f'https://top30mt.ru/api/v1/user/{student.user_id}/avatar' if user.has_photo else None,
                ) for user, student in zip(users, students.items)
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
        delete_student_case: domain.student.use_cases.delete.DeleteStudentFromRepo =
        Depends(dependencies.get__delete_student_from_repo),
        delete_user_case: domain.user.use_cases.delete.DeleteUserFromRepo =
        Depends(dependencies.get__delete_user_from_repo),
):
    await delete_student_case.delete(user_id=id)
    await delete_user_case.delete(id=id)
