from datetime import (
    datetime,
    timedelta,
)

from aiogram.types import CallbackQuery, Message
from aiogram_calendar import (
    SimpleCalendar,
    get_user_locale,
)


async def get_date_range() -> tuple[datetime, datetime]:
    now = datetime.now() - timedelta(days=1)
    max_date = datetime(
        year=(now.year + 2),
        month=now.month,
        day=now.day,
    )
    return now, max_date


async def get_calendar_keyboard(query_message: CallbackQuery | Message) -> SimpleCalendar:
    now, max_date = await get_date_range()
    calendar = SimpleCalendar(
        locale=await get_user_locale(query_message.from_user), show_alerts=True
    )
    calendar.set_dates_range(now, max_date)
    return calendar
