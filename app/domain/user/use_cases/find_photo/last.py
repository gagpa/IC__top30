from uuid import UUID

from domain.user.resources.user_photo_repo import UserPhotoRepo
from .base import FindPhoto


class FindLastPhoto(FindPhoto):

    def __init__(self, photo_repo: UserPhotoRepo):
        self.photo_repo = photo_repo

    async def find(self, user_id: UUID) -> bytes:
        return await self.photo_repo.find(user_id)
