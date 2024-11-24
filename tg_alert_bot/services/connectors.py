from typing import AsyncGenerator
from contextlib import asynccontextmanager

import aiohttp
import aio_pika
from aiogram import Bot
from redis.asyncio import Redis

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


@asynccontextmanager
async def get_cache_session() -> AsyncGenerator[Redis, None]:
    cache_session = Redis(
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
        db=config.REDIS_DB,
        decode_responses=True,
    )
    try:
        yield cache_session
    finally:
        await cache_session.aclose()
