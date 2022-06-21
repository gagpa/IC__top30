import pydantic
import pytest


@pytest.mark.asyncio
async def test_positive__add(add_user_in_repo, add_student_in_repo, user_entity, student_entity):
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
    assert new_student.user_id == new_user.id
    assert student_entity.position == new_student.position
    assert student_entity.organization == new_student.organization
    assert student_entity.experience == new_student.experience
    assert student_entity.lead == new_student.lead


@pytest.mark.asyncio
async def test_negative__already_exist(
        add_user_in_repo,
        add_student_in_repo,
        user_entity,
        student_entity,
        already_exist_error,
):
    new_user = await add_user_in_repo.add(
        first_name=user_entity.first_name,
        last_name=user_entity.last_name,
        email=user_entity.email,
        phone=user_entity.phone,
        photo=user_entity.photo,
    )
    await add_student_in_repo.add(
        user_id=new_user.id,
        position=student_entity.position,
        organization=student_entity.organization,
        experience=student_entity.experience,
        lead=student_entity.lead,
    )
    with pytest.raises(already_exist_error):
        await add_student_in_repo.add(
            user_id=new_user.id,
            position=student_entity.position,
            organization=student_entity.organization,
            experience=student_entity.experience,
            lead=student_entity.lead,
        )


@pytest.mark.asyncio
async def test_negative__user_not_founded(add_student_in_repo, student_entity, not_founded_error):
    with pytest.raises(not_founded_error):
        await add_student_in_repo.add(
            user_id=student_entity.user_id,
            position=student_entity.position,
            organization=student_entity.organization,
            experience=student_entity.experience,
            lead=student_entity.lead,
        )
