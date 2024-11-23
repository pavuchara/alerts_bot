from aiogram import Router
from aiogram.types import Message

from lexicon.lexicon import LEXICON


from aiogram.types import ReplyKeyboardRemove


router = Router()


@router.message()
async def process_all(message: Message):
    await message.reply(
        text=LEXICON["other"],
        reply_markup=ReplyKeyboardRemove()
    )
