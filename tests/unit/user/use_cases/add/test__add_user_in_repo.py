import pydantic
import pytest


@pytest.mark.asyncio
async def test_positive__add(add_user_in_repo, user_entity):
    new_user = await add_user_in_repo.add(
        first_name=user_entity.first_name,
        last_name=user_entity.last_name,
        email=user_entity.email,
        phone=user_entity.phone,
        photo=user_entity.photo,
    )
    assert user_entity.id != new_user.id
    assert user_entity.first_name == new_user.first_name
    assert user_entity.last_name == new_user.last_name
    assert user_entity.email == new_user.email
    assert user_entity.phone == new_user.phone
    assert user_entity.photo == new_user.photo


@pytest.mark.asyncio
async def test_negative__already_exist(add_user_in_repo, already_exist_error, user_entity):
    await add_user_in_repo.add(
        first_name=user_entity.first_name,
        last_name=user_entity.last_name,
        email=user_entity.email,
        phone=user_entity.phone,
        photo=user_entity.photo,
    )
    with pytest.raises(already_exist_error):
        await add_user_in_repo.add(
            first_name=user_entity.first_name,
            last_name=user_entity.last_name,
            email=user_entity.email,
            phone=user_entity.phone,
            photo=user_entity.photo,
        )


@pytest.mark.asyncio
async def test_negative__only_russian_phone(add_user_in_repo, user_entity):
    with pytest.raises(pydantic.ValidationError):
        add_user_in_repo.add(
            first_name=user_entity.first_name,
            last_name=user_entity.last_name,
            email=user_entity.email,
            phone='99999999',
            photo=user_entity.photo,
        )
