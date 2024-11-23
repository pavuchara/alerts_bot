import re
from datetime import datetime, timedelta

import pytz

from aiogram.filters import BaseFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext


class TimeFilter(BaseFilter):

    async def __call__(self, message: Message, state: FSMContext) -> bool:
        time_pattern = r"^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$"
        fit_pattern = bool(re.fullmatch(time_pattern, message.text))
        if not fit_pattern:
            return False
        timezone = pytz.timezone("Europe/Moscow")

        currrent_date = datetime.now(timezone) + timedelta(minutes=5)

        date_from_fsm: datetime = (await state.get_data())["date"]

        recived_date_naive = datetime(
            year=date_from_fsm.year,
            month=date_from_fsm.month,
            day=date_from_fsm.day,
            hour=int(message.text.split(":")[0]),
            minute=int(message.text.split(":")[1]),
        )
        recived_date = timezone.localize(recived_date_naive)
        if recived_date > currrent_date:
            return {"normalized_datetime": recived_date}
