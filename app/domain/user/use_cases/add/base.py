from abc import ABC

__all__ = ['AddUser']


class AddUser(ABC):
    """Бизнес логика добавления нового пользователя"""

    async def add(
            self, password: str, first_name: str, last_name: str, patronymic: str, phone: str, email: str, photo: str,
    ):
        """Добавить нового пользователя"""
