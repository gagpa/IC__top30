import pytest


@pytest.mark.asyncio
async def test_positive__delete(
        user_entity,
        student_entity,
        add_user_in_repo,
        add_student_in_repo,
        find_student_in_repo,
        student_deleter,
        not_founded_error,
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
    await student_deleter.delete(user_id=new_student.user_id)
    with pytest.raises(not_founded_error):
        assert await find_student_in_repo.find(user_id=new_student.user_id)
