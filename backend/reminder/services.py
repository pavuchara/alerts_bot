from abc import ABC, abstractmethod
from typing import Sequence

from reminder.exceptions import (
    ReminderDoesNotExistException,
    ReminderPermissionsException,
    ReminderLimitException,
)
from reminder.models import Reminder
from reminder.repositories import ReminderRepository
from reminder.schemas import (
    ReminderCreateSchema,
    ReminderUpdateSchema,
)


class AbstractReminderService(ABC):

    @abstractmethod
    async def get_all_reminders(self) -> Sequence[Reminder]:
        raise NotImplementedError

    @abstractmethod
    async def get_reminder_by_id(
        self,
        user_id: int,
        reminder_id: int,
        raise_not_found_exception: bool = True,
    ) -> Reminder | None:
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
        user_id: int,
        reminder_id: int,
        reminder_data: ReminderUpdateSchema
    ) -> Reminder | None:
        raise NotImplementedError

    @abstractmethod
    async def delete_reminder(self, user_id: int, reminder_id: int) -> None:
        raise NotImplementedError


class ReminderService(AbstractReminderService):

    def __init__(self, reminder_repository: ReminderRepository) -> None:
        self.reminder_repository = reminder_repository

    async def get_all_reminders(self) -> Sequence[Reminder]:
        return await self.reminder_repository.get_all_reminders()

    async def get_reminder_by_id(
        self,
        user_id: int,
        reminder_id: int,
        raise_not_found_exception: bool = True,
    ) -> Reminder | None:
        reminder = await self.reminder_repository.get_reminder_by_id(reminder_id=reminder_id)
        if not reminder and raise_not_found_exception:
            raise ReminderDoesNotExistException()
        if reminder and reminder.user_id != user_id:
            raise ReminderPermissionsException()
        return reminder

    async def get_reminders_by_user_id(self, user_id: int) -> Sequence[Reminder]:
        return await self.reminder_repository.get_reminders_by_user_id(user_id=user_id)

    async def create_reminder(self, reminder_data: ReminderCreateSchema, user_id: int) -> Reminder:
        if len(await self.get_reminders_by_user_id(user_id=user_id)) >= 10:
            raise ReminderLimitException()
        return await self.reminder_repository.create_reminder(
            reminder_data=reminder_data,
            user_id=user_id,
        )

    async def update_reminder(
        self,
        user_id: int,
        reminder_id: int,
        reminder_data: ReminderUpdateSchema,
    ) -> Reminder | None:
        reminder = await self.get_reminder_by_id(user_id=user_id, reminder_id=reminder_id)
        return await self.reminder_repository.update_reminder(
            reminder=reminder,  # type: ignore
            reminder_data=reminder_data,
        )

    async def delete_reminder(self, user_id: int,  reminder_id: int) -> None:
        reminder = await self.get_reminder_by_id(user_id=user_id, reminder_id=reminder_id)
        return await self.reminder_repository.delete_reminder(reminder=reminder)
