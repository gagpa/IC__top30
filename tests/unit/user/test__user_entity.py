def test_positive__create(user_entity):
    assert isinstance(user_entity.first_name, str)
    assert isinstance(user_entity.last_name, str)
    assert isinstance(user_entity.email, str)
    assert isinstance(user_entity.phone, str)
    assert user_entity.photo is None or isinstance(user_entity.photo, str)
