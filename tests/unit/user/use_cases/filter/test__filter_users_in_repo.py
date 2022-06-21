import pytest


@pytest.mark.asyncio
async def test_positive__all(user_entity, add_user_in_repo, filter_user_in_repo):
    new_user = await add_user_in_repo.add(
        first_name=user_entity.first_name,
        last_name=user_entity.last_name,
        email=user_entity.email,
        phone=user_entity.phone,
        photo=user_entity.photo,
    )
    users = await filter_user_in_repo.filter(page=0)
    assert [new_user] == users.items
