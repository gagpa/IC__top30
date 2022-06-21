import typing
import uuid

import pydantic
import pytest

from app import domain, errors


@pytest.fixture
def already_exist_error():
    return errors.EntityAlreadyExist


@pytest.fixture
def not_founded_error():
    return errors.EntityNotFounded


@pytest.fixture()
def user_entity():
    """Сущность пользователя"""
    return domain.user.entity.UserEntity(
        id=uuid.uuid4(),
        first_name='Test',
        last_name='Faker',
        email=pydantic.EmailStr('test@faker.ru'),
        phone='+79876543210',
        photo=None,
    )


@pytest.fixture()
def add_user_in_repo(user_repo):
    return domain.user.use_cases.add.AddUserInRepo(user_repo=user_repo)


@pytest.fixture()
def find_user_in_repo(user_repo):
    return domain.user.use_cases.find.FindUserInRepo(user_repo=user_repo)


@pytest.fixture()
def user_storage():
    return {}


@pytest.fixture()
def user_repo(already_exist_error, user_storage):
    class TestUserRepo(domain.user.resources.repo.UserRepo):

        def __init__(self, storage: dict):
            self.storage = storage

        async def add(
                self,
                first_name: str,
                last_name: str,
                phone: str,
                email: pydantic.EmailStr,
                photo: typing.Optional[str] = None
        ) -> domain.user.entity.UserEntity:
            if [user.email for user in self.storage.values() if user.email == email]:
                raise already_exist_error()
            new_id = uuid.uuid4()
            self.storage[new_id] = domain.user.entity.UserEntity(
                id=new_id,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                email=email,
                photo=photo,
            )
            return self.storage[new_id]

        async def find(self, id: uuid.UUID):
            try:
                return self.storage[id]
            except KeyError:
                raise errors.EntityNotFounded()

        async def filter(self, page: int = 0) -> domain.user.entity.ListUserEntity:
            items = list(self.storage.values())
            return domain.user.entity.ListUserEntity(
                total=len(items),
                max_page=0,
                items=items,
            )

    return TestUserRepo(user_storage)


@pytest.fixture()
def user_deleter(not_founded_error, user_storage):
    class TestUserDeleter(domain.user.resources.deleter.UserDeleter):

        def __init__(self, storage: dict):
            self.storage = storage

        async def delete(self, id: uuid.UUID):
            try:
                self.storage.pop(id)
            except KeyError:
                raise not_founded_error()

    return TestUserDeleter(user_storage)


@pytest.fixture()
def delete_user_from_repo(user_deleter):
    return domain.user.use_cases.delete.DeleteUserFromRepo(user_deleter=user_deleter)


@pytest.fixture()
def filter_user_in_repo(user_repo):
    return domain.user.use_cases.filter.FilterUserInRepo(user_repo=user_repo)


@pytest.fixture()
def student_entity():
    return domain.student.StudentEntity(
        user_id=uuid.uuid4(),
        position='Большой начальник',
        organization='ЦОДД',
        experience='40 лет',
        lead='Иван Иванович',
    )


@pytest.fixture()
def student_storage():
    return {}


@pytest.fixture()
def student_repo(student_storage, user_storage, already_exist_error, not_founded_error):
    class TestStudentRepo(domain.student.resources.repo.StudentRepo):

        def __init__(self, storage: dict, user_storage: dict):
            self.storage = storage
            self.user_storage = user_storage

        async def add(
                self,
                user_id: uuid.UUID,
                position: str,
                organization: str,
                experience: str,
                lead: str,
        ) -> domain.student.StudentEntity:
            if user_id in self.storage:
                raise already_exist_error()
            if user_id not in self.user_storage:
                raise not_founded_error()
            self.storage[user_id] = domain.student.StudentEntity(
                user_id=user_id,
                position=position,
                organization=organization,
                experience=experience,
                lead=lead,
            )
            return self.storage[user_id]

        async def find(self, user_id: uuid.UUID):
            try:
                return self.storage[user_id]
            except KeyError:
                raise errors.EntityNotFounded()

        async def filter(self, page: int = 0) -> domain.user.entity.ListUserEntity:
            items = list(self.storage.values())
            return domain.student.entity.ListStudentEntity(
                total=len(items),
                max_page=0,
                items=items,
            )

    return TestStudentRepo(student_storage, user_storage)


@pytest.fixture()
def add_student_in_repo(student_repo):
    return domain.student.use_cases.add.AddStudentInRepo(student_repo=student_repo)


@pytest.fixture()
def find_student_in_repo(student_repo):
    return domain.student.use_cases.find.FindStudentInRepo(student_repo=student_repo)


@pytest.fixture()
def student_deleter(not_founded_error, student_storage):
    class TestStudentDeleter(domain.student.resources.deleter.StudentDeleter):

        def __init__(self, storage: dict):
            self.storage = storage
            self.user_storage = user_storage

        async def delete(self, user_id: uuid.UUID):
            try:
                self.storage.pop(user_id)
            except KeyError:
                raise not_founded_error()

    return TestStudentDeleter(student_storage)


@pytest.fixture()
def delete_student_from_repo(student_deleter):
    return domain.student.use_cases.delete.DeleteStudentFromRepo(student_deleter=student_deleter)


@pytest.fixture()
def filter_students_from_repo(student_repo):
    return domain.student.use_cases.filter.FilterStudentsFromRepo(student_repo=student_repo)


@pytest.fixture()
def coach_entity():
    return domain.coach.CoachEntity(
        user_id=uuid.uuid4(),
        profession='Разработчик ракет и космических аппаратов',
        specialization='Руководитель отдела',
        experience='1 день',
        key_specializations='Тайм-менеджмент, продажи',
    )


@pytest.fixture()
def coach_storage():
    return {}


@pytest.fixture()
def coach_repo(coach_storage, user_storage, already_exist_error, not_founded_error):
    class TestCoachRepo(domain.coach.resources.repo.CoachRepo):

        def __init__(self, storage: dict, user_storage: dict):
            self.storage = storage
            self.user_storage = user_storage

        async def add(
                self,
                user_id: uuid.UUID,
                profession: str,
                specialization: str,
                experience: str,
                key_specializations: str,
        ) -> domain.coach.CoachEntity:
            if user_id in self.storage:
                raise already_exist_error()
            if user_id not in self.user_storage:
                raise not_founded_error()
            self.storage[user_id] = domain.coach.CoachEntity(
                user_id=user_id,
                profession=profession,
                specialization=specialization,
                experience=experience,
                key_specializations=key_specializations,
            )
            return self.storage[user_id]

        async def find(self, user_id: uuid.UUID):
            try:
                return self.storage[user_id]
            except KeyError:
                raise errors.EntityNotFounded()

        async def filter(self, page: int = 0) -> domain.user.entity.ListUserEntity:
            items = list(self.storage.values())
            return domain.coach.entity.ListCoachEntity(
                total=len(items),
                max_page=0,
                items=items,
            )

    return TestCoachRepo(coach_storage, user_storage)


@pytest.fixture()
def add_coach_in_repo(coach_repo):
    return domain.coach.use_cases.add.AddCoachInRepo(coach_repo=coach_repo)


@pytest.fixture()
def find_coach_in_repo(coach_repo):
    return domain.coach.use_cases.find.FindCoachInRepo(coach_repo=coach_repo)


@pytest.fixture()
def coach_deleter(not_founded_error, coach_storage):
    class TestCoachDeleter(domain.coach.resources.deleter.CoachDeleter):

        def __init__(self, storage: dict):
            self.storage = storage
            self.user_storage = user_storage

        async def delete(self, user_id: uuid.UUID):
            try:
                self.storage.pop(user_id)
            except KeyError:
                raise not_founded_error()

    return TestCoachDeleter(coach_storage)


@pytest.fixture()
def delete_coach_from_repo(coach_deleter):
    return domain.coach.use_cases.delete.DeleteCoachFromRepo(coach_deleter=coach_deleter)


@pytest.fixture()
def filter_coachs_from_repo(coach_repo):
    return domain.coach.use_cases.filter.FilterCoachsFromRepo(coach_repo=coach_repo)
