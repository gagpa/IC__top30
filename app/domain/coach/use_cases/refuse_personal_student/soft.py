from datetime import datetime, timedelta
from uuid import UUID

from domain.event.entity import EventStatus
from domain.event.resources.deleter import EventDeleter
from domain.event.resources.repo import EventRepo
from domain.event.resources.slot_cleaner import SlotCleaner
from domain.event.resources.stutus_changer import EventStatusChanger
from domain.student.resources.personal_coach_changer import PersonalCoachChanger
from domain.student.resources.student_repo import StudentRepo
from .base import RefusePersonalStudent


class SoftRefusePersonalStudent(RefusePersonalStudent):

    def __init__(
            self,
            student_repo: StudentRepo,
            coach_changer: PersonalCoachChanger,
            event_deleter: EventDeleter,
            event_repo: EventRepo,
            slot_cleaner: SlotCleaner,
            event_status_changer: EventStatusChanger,
    ):
        self.student_repo = student_repo
        self.coach_changer = coach_changer
        self.event_deleter = event_deleter
        self.event_repo = event_repo
        self.slot_cleaner = slot_cleaner
        self.event_status_changer = event_status_changer

    async def refuse(self, student_id: UUID):
        student = await self.student_repo.find(student_id)
        events = await self.event_repo.filter(student_id=student_id, coach_id=None)
        for event in events.items:
            time_for_event = event.start_date - datetime.now()
            if time_for_event != abs(time_for_event):
                return
            if time_for_event < timedelta(hours=24):
                print(time_for_event)
                await self.event_status_changer.change(status=EventStatus.burned, event_id=event.id)
            else:
                await self.event_deleter.delete(event_id=event.id)
            await self.slot_cleaner.clean(event.id)
        await self.coach_changer.change(student.user_id, new_coach=None)
