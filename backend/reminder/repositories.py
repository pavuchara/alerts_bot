from abc import ABC, abstractmethod
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from reminder.models import Reminder
from reminder.schemas import (
    ReminderCreateSchema,
    ReminderUpdateSchema,
)


class AbstractReminderRepository(ABC):

    @abstractmethod
    async def get_all_reminders(self) -> Sequence[Reminder]:
        raise NotImplementedError

    @abstractmethod
    async def get_reminder_by_id(self, reminder_id: int) -> Reminder | None:
        raise NotImplementedError

    @abstractmethod
    async def get_reminders_by_user_id(self, user_id: int) -> Sequence[Reminder]:
        raise NotImplementedError

    @abstractmethod
    async def create_reminder(self, reminder_data: ReminderCreateSchema, user_id: int) -> Reminder:
        raise NotImplementedError

    @abstractmethod
    async def update_reminder(
        self,
        reminder: Reminder,
        reminder_data: ReminderUpdateSchema
    ) -> Reminder:
        raise NotImplementedError

    @abstractmethod
    async def delete_reminder(self, reminder: Reminder) -> None:
        raise NotImplementedError


class ReminderRepository(AbstractReminderRepository):

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_reminders(self) -> Sequence[Reminder]:
        reminders = await self.db.scalars(select(Reminder))
        return reminders.all()

    async def get_reminder_by_id(self, reminder_id: int) -> Reminder | None:
        reminder = await self.db.scalar(
            select(Reminder)
            .where(Reminder.id == reminder_id)
        )
        return reminder

    async def get_reminders_by_user_id(self, user_id: int) -> Sequence[Reminder]:
        reminders = await self.db.scalars(
            select(Reminder)
            .where(Reminder.user_id == user_id)
        )
        return reminders.all()

    async def create_reminder(self, reminder_data: ReminderCreateSchema, user_id: int) -> Reminder:
        reminder = Reminder(
            user_id=user_id,
            alert_datetime=reminder_data.alert_datetime,
            description=reminder_data.description,
        )
        self.db.add(reminder)
        await self.db.commit()
        await self.db.refresh(reminder)
        return reminder

    async def update_reminder(
        self,
        reminder: Reminder,
        reminder_data: ReminderUpdateSchema,
    ) -> Reminder:
        reminder.alert_datetime = reminder_data.alert_datetime
        reminder.description = reminder_data.description
        self.db.add(reminder)
        await self.db.commit()
        return reminder

    async def delete_reminder(self, reminder: Reminder | None) -> None:
        if reminder:
            await self.db.delete(reminder)
            await self.db.commit()
