from uuid import UUID


def test_positive__create(student_entity):
    assert isinstance(student_entity.user_id, UUID)
    assert isinstance(student_entity.position, str)
    assert isinstance(student_entity.organization, str)
    assert isinstance(student_entity.experience, str)
    assert isinstance(student_entity.lead, str)
