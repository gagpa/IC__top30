import pytest


@pytest.mark.asyncio
async def test_positive__find_student_in_repo(
        user_entity, student_entity, add_user_in_repo, add_student_in_repo, find_student_in_repo,
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
    student_from_repo = await find_student_in_repo.find(new_student.user_id)
    assert new_student.user_id == student_from_repo.user_id


@pytest.mark.asyncio
async def test_negative__not_founded(student_entity, find_student_in_repo, not_founded_error):
    with pytest.raises(not_founded_error):
        await find_student_in_repo.find(user_id=student_entity.user_id)
