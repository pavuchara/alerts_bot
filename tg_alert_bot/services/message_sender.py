import json
import aio_pika
from aiogram import Bot

from handlers.message_senders import send_message


class ReminderTGMessageSender:

    def __init__(self, bot: Bot) -> None:
        self.__bot = bot

    async def process_message_notificator(self, message: aio_pika.IncomingMessage):
        chat_id, prepared_message = await self.__prepare_message(message=message)
        await send_message(self.__bot, chat_id, prepared_message)
        await message.ack()

    async def __prepare_message(self, message: aio_pika.IncomingMessage):
        decoded_message = json.loads(message.body.decode())
        chat_id, recived_message = decoded_message["tg_id"], decoded_message["description"]
        prepared_message = f"Ты просил/а напомнить:\n'{recived_message}'"
        return chat_id, prepared_message
