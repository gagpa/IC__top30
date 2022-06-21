from domain.coach.resources.deleter import CoachDeleter
from .base import DeleteCoach
from uuid import UUID

__all__ = ['DeleteCoachFromRepo']


class DeleteCoachFromRepo(DeleteCoach):
    """Бизнес логика удаления коуча из репозитория"""

    def __init__(self, coach_deleter: CoachDeleter):
        self.coach_deleter = coach_deleter

    async def delete(self, user_id: UUID):
        await self.coach_deleter.delete(user_id)
