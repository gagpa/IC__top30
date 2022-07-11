from uuid import UUID

from domain.user.resources.repo import UserRepo
from domain.user.resources.user_photo_repo import UserPhotoRepo
from .base import AddPhoto


class AddPhotoInRepo(AddPhoto):

    def __init__(self, user_repo: UserRepo, user_photo_repo: UserPhotoRepo):
        self.user_photo_repo = user_photo_repo
        self.user_repo = user_repo

    async def add(self, user_id: UUID, photo: bytes):
        """Добавить фотографию пользователю в репозиторий"""
        user = await self.user_repo.find(user_id)
        await self.user_photo_repo.add(user_id=user.id, photo=photo)
