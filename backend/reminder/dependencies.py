from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.db_depends import get_db_session
from reminder.repositories import ReminderRepository
from reminder.services import ReminderService


async def get_reminder_repository(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
) -> ReminderRepository:
    return ReminderRepository(db_session)


async def get_reminder_service(
    reminder_repository: Annotated[ReminderRepository, Depends(get_reminder_repository)]
) -> ReminderService:
    return ReminderService(reminder_repository=reminder_repository)
