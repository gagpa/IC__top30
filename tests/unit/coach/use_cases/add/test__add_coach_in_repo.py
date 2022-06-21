import pydantic
import pytest


@pytest.mark.asyncio
async def test_positive__add(add_user_in_repo, add_coach_in_repo, user_entity, coach_entity):
    new_user = await add_user_in_repo.add(
        first_name=user_entity.first_name,
        last_name=user_entity.last_name,
        email=user_entity.email,
        phone=user_entity.phone,
        photo=user_entity.photo,
    )
    new_coach = await add_coach_in_repo.add(
        user_id=new_user.id,
        profession=coach_entity.profession,
        specialization=coach_entity.specialization,
        experience=coach_entity.experience,
        key_specializations=coach_entity.key_specializations,
    )
    assert new_coach.user_id == new_user.id
    assert coach_entity.profession == new_coach.profession
    assert coach_entity.specialization == new_coach.specialization
    assert coach_entity.experience == new_coach.experience
    assert coach_entity.key_specializations == new_coach.key_specializations


@pytest.mark.asyncio
async def test_negative__already_exist(
        add_user_in_repo,
        add_coach_in_repo,
        user_entity,
        coach_entity,
        already_exist_error,
):
    new_user = await add_user_in_repo.add(
        first_name=user_entity.first_name,
        last_name=user_entity.last_name,
        email=user_entity.email,
        phone=user_entity.phone,
        photo=user_entity.photo,
    )
    await add_coach_in_repo.add(
        user_id=new_user.id,
        profession=coach_entity.profession,
        specialization=coach_entity.specialization,
        experience=coach_entity.experience,
        key_specializations=coach_entity.key_specializations,
    )
    with pytest.raises(already_exist_error):
        await add_coach_in_repo.add(
            user_id=new_user.id,
            profession=coach_entity.profession,
            specialization=coach_entity.specialization,
            experience=coach_entity.experience,
            key_specializations=coach_entity.key_specializations,
        )


@pytest.mark.asyncio
async def test_negative__user_not_founded(add_coach_in_repo, coach_entity, not_founded_error):
    with pytest.raises(not_founded_error):
        await add_coach_in_repo.add(
            user_id=coach_entity.user_id,
            profession=coach_entity.profession,
            specialization=coach_entity.specialization,
            experience=coach_entity.experience,
            key_specializations=coach_entity.key_specializations,
        )
