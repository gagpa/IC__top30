from datetime import datetime, timedelta
from uuid import UUID
import errors
from domain.event.entity import EventEntity
from domain.event.resources.mover import EventMover
from domain.event.resources.repo import EventRepo
from domain.slot.resources.repo import SlotRepo
from domain.student.resources.student_repo import StudentRepo
from .base import MoveEvent


class MoveEventAsGod(MoveEvent):

    def __init__(self, event_mover: EventMover, event_repo: EventRepo, slot_repo: SlotRepo, student_repo: StudentRepo):
        self.event_repo = event_repo
        self.event_mover = event_mover
        self.slot_repo = slot_repo
        self.student_repo = student_repo

    async def move(self, event_id: UUID, new_start_date: datetime) -> EventEntity:
        event = await self.event_repo.find(event_id=event_id)
        event_duration = event.end_date - event.start_date
        student = await self.student_repo.find(event.student)
        requirement_slots_count = abs(int(event_duration.seconds / 60 / 60))
        for i in range(requirement_slots_count):
            start_date = new_start_date + timedelta(hours=i)
            available_slot = await self.slot_repo.filter(
                start_date=start_date,
                end_date=None,
                coach_id=student.coach_id,
                student_id=None,
                is_free=True,
            )
            if not available_slot.items:
                print(f'START: {start_date}')
                print(f'END: {start_date + timedelta(hours=1)}')
                await self.slot_repo.add(
                    student.coach_id,
                    start_date=start_date,
                    end_date=start_date + timedelta(hours=1),
                )
        await self.slot_repo.session.execute()
        return await self.event_mover.move(event_id=event.id, new_start_date=new_start_date)
