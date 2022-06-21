import pytest


@pytest.mark.asyncio
async def test_positive__delete(
        user_entity,
        coach_entity,
        add_user_in_repo,
        add_coach_in_repo,
        find_coach_in_repo,
        coach_deleter,
        not_founded_error,
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
    await coach_deleter.delete(user_id=new_coach.user_id)
    with pytest.raises(not_founded_error):
        assert await find_coach_in_repo.find(user_id=new_coach.user_id)
