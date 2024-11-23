import asyncio

from aiogram import Bot


async def send_message(bot: Bot, chat_id: int | str, prepared_message: str):
    await bot.send_message(chat_id=chat_id, text=prepared_message)
    # Barier when something went wrong...
    await asyncio.sleep(0.1)
