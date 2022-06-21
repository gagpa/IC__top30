from uuid import UUID


def test_positive__create(coach_entity):
    assert isinstance(coach_entity.user_id, UUID)
    assert isinstance(coach_entity.profession, str)
    assert isinstance(coach_entity.specialization, str)
    assert isinstance(coach_entity.experience, str)
    assert isinstance(coach_entity.key_specializations, str)
