import typing

from domain.user.entity import UserEntity
from domain.auth.resources.password_hasher import PasswordHasher
from domain.user.resources.repo.base import UserRepo
from .base import AddUser

__all__ = ['AddUserInRepo']


class AddUserInRepo(AddUser):
    """Бизнес логика добавления нового пользователя в репозиторий"""

    def __init__(self, user_repo: UserRepo, password_hasher: PasswordHasher):
        self.user_repo = user_repo
        self.password_hasher = password_hasher

    async def add(
            self,
            password: str,
            first_name: str,
            last_name: str,
            patronymic: str,
            phone: str,
            email: str,
            photo: typing.Optional[str] = None,
    ) -> UserEntity:
        """Добавить"""
        hashed_password = self.password_hasher.hashed(password)
        return await self.user_repo.add(
            password=hashed_password,
            first_name=first_name,
            last_name=last_name,
            patronymic=patronymic,
            phone=phone,
            email=email,
            photo=photo,
        )
