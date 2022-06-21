import pytest


@pytest.mark.asyncio
async def test_positive__find_coach_in_repo(
        user_entity, coach_entity, add_user_in_repo, add_coach_in_repo, find_coach_in_repo,
):
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
    coach_from_repo = await find_coach_in_repo.find(new_coach.user_id)
    assert new_coach.user_id == coach_from_repo.user_id


@pytest.mark.asyncio
async def test_negative__not_founded(coach_entity, find_coach_in_repo, not_founded_error):
    with pytest.raises(not_founded_error):
        await find_coach_in_repo.find(user_id=coach_entity.user_id)
