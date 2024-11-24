from datetime import datetime

from aiogram import Router, F
from aiogram.types import (
    Message,
    CallbackQuery,

)
from aiogram.filters import (
    Command,
    CommandStart,
    StateFilter,
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from aiogram_calendar import SimpleCalendarCallback
from aiogram_calendar.schemas import SimpleCalAct

from lexicon.lexicon import LEXICON
from filters.time_filter import TimeFilter
from services.backend.exceptions import (
    ReminderServiceException,
    ReminderLimitException,
)
from state_machine.reminder import FSMFillReminder
from keyboards.calendar_keyboard import get_calendar_keyboard
from keyboards.reminder_keyboards import (
    create_inline_reminder_kb,
    create_edit_reminder_keyboard,
)
from services.backend.reminder_service import ReminderService

router = Router()

user_dict: dict = {}


@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer(LEXICON["/start"])


@router.message(Command("help"), StateFilter(default_state))
async def process_help_command(message: Message):  # TEST
    await message.answer(LEXICON["/help"])


@router.message(Command("cancel"), StateFilter(default_state))
async def process_cancel_wo_fsm(message: Message):
    """`/cancel` wo FSM."""
    await message.answer(LEXICON["cancel_wo_fsm"])


@router.message(Command("cancel"), ~StateFilter(default_state))
async def process_cancel_in_fsm(message: Message, state: FSMContext):
    """`/cancel` in FSM."""
    await message.answer(LEXICON["/cancel"])
    await state.clear()


@router.message(Command("create"), StateFilter(default_state))
async def process_create_wo_fsm(
    message: Message,
    state: FSMContext,
    reminder_service: ReminderService,
):
    """Entry point for FSM fill reminder."""
    if len(await reminder_service.get_self_reminders()) >= 10:
        await message.answer(text=LEXICON["reminder_limit"])
    else:
        calendar = await get_calendar_keyboard(message)
        await message.answer(
            text=LEXICON["/create"],
            reply_markup=await calendar.start_calendar()
        )
        await state.set_state(FSMFillReminder.fill_date)


@router.callback_query(
    SimpleCalendarCallback.filter(F.act.not_in({SimpleCalAct.cancel, SimpleCalAct.ignore})),
    StateFilter(FSMFillReminder.fill_date),
)
async def process_simple_calendar(
    callback_query: CallbackQuery,
    callback_data: SimpleCalendarCallback,
    state: FSMContext,
):
    """Fill date with calendar keyboard."""
    calendar = await get_calendar_keyboard(callback_query)
    selected, date = await calendar.process_selection(callback_query, callback_data)
    if selected:
        await state.update_data(date=date)
        await callback_query.message.answer(text=LEXICON["filled_date"])  # type: ignore
        await state.set_state(FSMFillReminder.fill_time)


@router.callback_query(
    SimpleCalendarCallback.filter(F.act.in_({SimpleCalAct.cancel, SimpleCalAct.ignore})),
    StateFilter(FSMFillReminder.fill_date),
)
async def process_cancel_or_ignore(callback_query: CallbackQuery, state: FSMContext):
    """`cancell` button in calendar."""
    await callback_query.message.answer(LEXICON["cancelled_date_fill"])
    await callback_query.message.delete()
    await state.clear()


@router.message(StateFilter(FSMFillReminder.fill_date))
async def process_any_on_fill_date(message: Message):
    """All `wrong` messages while fill date."""
    await message.answer(LEXICON["wrog_date"])


@router.message(
    StateFilter(FSMFillReminder.fill_time),
    TimeFilter(),
)
async def process_fill_time(message: Message, state: FSMContext, normalized_datetime: datetime):
    """Fill time py re pattern."""
    await state.update_data(time=message.text)
    await state.update_data(normalized_datetime=normalized_datetime)
    await message.answer(text=LEXICON["filled_time"])
    await state.set_state(FSMFillReminder.fill_description)


@router.message(StateFilter(FSMFillReminder.fill_time))
async def process_wrong_time(message: Message):
    """Any wrong message while fill time."""
    await message.answer(text=LEXICON["wrog_time"])


@router.message(
    StateFilter(FSMFillReminder.fill_description),
    F.text.len() <= 255,
    ~F.text.startswith("/")
)
async def process_fill_description(
    message: Message,
    state: FSMContext,
    reminder_service: ReminderService,
):
    """Fill description (last step)."""
    await state.update_data(description=message.text)
    data = await state.get_data()
    try:
        await reminder_service.create_reminder(await state.get_data())
    except ReminderServiceException as e:
        await message.answer(text=str(e))
    except ReminderLimitException:
        await message.answer(text=LEXICON["reminder_limit"])
    else:
        await message.answer(
            text=LEXICON["filled_all_data"].format(date=data["date"].date(), time=data["time"])
        )
    finally:
        await state.clear()


@router.message(StateFilter(FSMFillReminder.fill_description))
async def process_fill_wrong_description(message: Message):
    """Any wrong message while process fill description."""
    await message.answer(text=LEXICON["wrong_description"])


@router.message(Command(commands="all"))
async def process_get_all_reminders(message: Message, reminder_service: ReminderService):
    """Check oll self reminders."""
    try:
        user_reminders = await reminder_service.get_self_reminders()
        if not user_reminders:
            await message.answer(text="Пусто!")
        else:
            keyboard = await create_inline_reminder_kb(*user_reminders)
            await message.answer(
                text="Все напоминания:",
                reply_markup=keyboard,
            )
    except ReminderServiceException as e:
        await message.answer(text=str(e))


@router.callback_query(F.data == "cancel")
async def process_cancel_all_reminders(callback_query: CallbackQuery):
    await callback_query.message.delete()


@router.callback_query(F.data == "edit_reminders")
async def process_edit_press(callback: CallbackQuery, reminder_service: ReminderService):
    """Edit(delete) reminders"""
    try:
        user_reminders = await reminder_service.get_self_reminders()
        keyboard = await create_edit_reminder_keyboard(*user_reminders)
        await callback.message.edit_text(text=LEXICON["deliting_reminders"], reply_markup=keyboard)
    except ReminderServiceException as e:
        await callback.message.answer(text=str(e))


@router.callback_query(F.data.startswith("DEL "))
async def process_delete_remider(callback: CallbackQuery, reminder_service: ReminderService):
    """Click DEL button."""
    reminder_id: int = int(callback.data.split(" ")[1])
    try:
        await reminder_service.delete_reminder_by_id(reminder_id=reminder_id)
        user_reminders = await reminder_service.get_self_reminders()
        if user_reminders:
            await callback.message.edit_text(
                text=LEXICON["deliting_reminders"],
                reply_markup=await create_edit_reminder_keyboard(*user_reminders)
            )
        else:
            await callback.message.edit_text(
                text=LEXICON["empty_reminders"],
                reply_markup=await create_edit_reminder_keyboard(*user_reminders)
            )
    except ReminderServiceException as e:
        await callback.message.answer(text=str(e))
