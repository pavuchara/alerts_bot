from aiogram.fsm.state import State, StatesGroup


class FSMFillReminder(StatesGroup):
    fill_date = State()
    fill_time = State()
    fill_description = State()
