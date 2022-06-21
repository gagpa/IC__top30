import pytest


@pytest.mark.asyncio
async def test_positive__find(user_entity, add_user_in_repo, find_user_in_repo):
    new_user = await add_user_in_repo.add(
        first_name=user_entity.first_name,
        last_name=user_entity.last_name,
        email=user_entity.email,
        phone=user_entity.phone,
        photo=user_entity.photo,
    )
    user_from_repo = await find_user_in_repo.find(id=new_user.id)
    assert user_from_repo.id == new_user.id


@pytest.mark.asyncio
async def test_negative__not_founded(user_entity, find_user_in_repo, not_founded_error):
    with pytest.raises(not_founded_error):
        await find_user_in_repo.find(id=user_entity.id)
