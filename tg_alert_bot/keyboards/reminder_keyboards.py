from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon import LEXICON


async def create_inline_reminder_kb(*buttons):
    kb_builder = InlineKeyboardBuilder()

    buttons_row = [
        InlineKeyboardButton(
            text=f"{button["message"]}",
            callback_data=button["reminder_id"],
        )
        for idx, button in enumerate(buttons, start=1)
    ]
    kb_builder.row(*buttons_row, width=1)

    management_row = [
        InlineKeyboardButton(
            text=LEXICON["edit_reminders_button"],
            callback_data="edit_reminders",
        ),
        InlineKeyboardButton(
            text=LEXICON["cancel"],
            callback_data="cancel",
        ),
    ]

    kb_builder.row(*management_row, width=2)
    return kb_builder.as_markup()


async def create_edit_reminder_keyboard(*buttons):
    kb_builder = InlineKeyboardBuilder()

    buttons_row = [
        InlineKeyboardButton(
            text=f"{LEXICON["del"]} {button["message"]}",
            callback_data=f"DEL {button["reminder_id"]}",
        )
        for idx, button in enumerate(buttons, start=1)
    ]
    kb_builder.row(*buttons_row, width=1)

    management_row = [
        InlineKeyboardButton(
            text=LEXICON["cancel"],
            callback_data="cancel",
        )
    ]
    kb_builder.row(*management_row, width=2)
    return kb_builder.as_markup()
