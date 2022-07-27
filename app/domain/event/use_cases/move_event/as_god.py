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
        available_slots = await self.slot_repo.filter(
            start_date=new_start_date,
            end_date=new_start_date + event_duration,
            coach_id=student.coach_id,
            student_id=None,
            is_free=True,
        )
        requirement_slots_count = abs(int(event_duration.seconds / 60 / 60))
        print(len(available_slots.items), requirement_slots_count)
        if len(available_slots.items) < requirement_slots_count:
            for i in range(requirement_slots_count):
                start_date = new_start_date + timedelta(hours=i)
                try:
                    await self.slot_repo.add(
                        student.coach_id,
                        start_date=start_date,
                        end_date=start_date + timedelta(hours=1),
                    )
                except errors.EntityAlreadyExist:
                    print(f'Slot exist - {start_date}')
                    continue
        return await self.event_mover.move(event_id=event.id, new_start_date=new_start_date)
