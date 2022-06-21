import pytest


@pytest.mark.asyncio
async def test_positive__filter_student_from_repo(
        user_entity, student_entity, add_user_in_repo, add_student_in_repo, student_repo, filter_students_from_repo,
):
    new_user = await add_user_in_repo.add(
        first_name=user_entity.first_name,
        last_name=user_entity.last_name,
        email=user_entity.email,
        phone=user_entity.phone,
        photo=user_entity.photo,
    )
    new_student = await add_student_in_repo.add(
        user_id=new_user.id,
        position=student_entity.position,
        organization=student_entity.organization,
        experience=student_entity.experience,
        lead=student_entity.lead,
    )
    students = await filter_students_from_repo.filter(page=0)
    assert students.items == [new_student]
