import pytest


@pytest.mark.asyncio
async def test_positive__delete(
        add_user_in_repo,
        find_user_in_repo,
        delete_user_from_repo,
        user_entity,
        not_founded_error,
):
    new_user = await add_user_in_repo.add(
        first_name=user_entity.first_name,
        last_name=user_entity.last_name,
        email=user_entity.email,
        phone=user_entity.phone,
        photo=user_entity.photo,
    )
    assert await find_user_in_repo.find(new_user.id)
    await delete_user_from_repo.delete(new_user.id)
    with pytest.raises(not_founded_error):
        await find_user_in_repo.find(new_user.id)


@pytest.mark.asyncio
async def test_negative__not_founded(delete_user_from_repo, user_entity, not_founded_error):
    with pytest.raises(not_founded_error):
        await delete_user_from_repo.delete(user_entity.id)
