from typing import AsyncGenerator
from contextlib import asynccontextmanager

import aiohttp
import aio_pika
from aiogram import Bot

import config
from services.message_sender import ReminderTGMessageSender


@asynccontextmanager
async def get_session() -> AsyncGenerator[aiohttp.ClientSession, None]:
    """Aihttp session."""
    session = aiohttp.ClientSession()
    try:
        yield session
    finally:
        await session.close()


async def amqp_consume_queue(bot: Bot):
    """Rabbitmq connection to recive messages from queue."""
    connection = await aio_pika.connect_robust(config.AMQP_URL)
    channel = await connection.channel()
    queue = await channel.declare_queue(
        name=config.REMINDER_ROUTING_KEY,
        durable=True,
    )
    sender = ReminderTGMessageSender(bot=bot)
    await queue.consume(sender.process_message_notificator)
