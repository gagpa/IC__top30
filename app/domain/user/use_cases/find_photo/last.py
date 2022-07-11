from .base import FindPhoto
from domain.user.resources.repo import UserRepo
from uuid import UUID


class FindLastPhoto(FindPhoto):

    def __init__(self, user_repo: UserRepo):
        self.user_repo = user_repo

    async def find(self, user_id: UUID) -> bytes:
        user = await self.user_repo.find(user_id)
        return bytes(user.photo)
