from uuid import UUID

from domain.user.resources.repo import UserRepo
from domain.user.resources.user_photo_deleter import UserPhotoDeleter
from .base import DeleteUserPhoto


class DeleteUserPhotoFromRepo(DeleteUserPhoto):

    def __init__(self, user_repo: UserRepo, user_photo_deleter: UserPhotoDeleter):
        self.user_repo = user_repo
        self.user_photo_deleter = user_photo_deleter

    async def delete(self, user_id: UUID):
        user = await self.user_repo.find(user_id)
        await self.user_photo_deleter.delete(user.id)
