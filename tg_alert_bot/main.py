import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

import config
from handlers import (
    other_handlers,
    user_handlers,
)
from keyboards.main_menu import set_main_menu
from middlewares.auth_middlware import AuthMiddleware
from middlewares.reminder_service_middleware import ReminderServiceMiddleware
from services.connectors import amqp_consume_queue


log = logging.getLogger(__name__)


async def main() -> None:
    config.configure_logging()

    bot: Bot = Bot(config.BOT_TOKEN)
    storage: MemoryStorage = MemoryStorage()

    dp: Dispatcher = Dispatcher(storage=storage)

    await set_main_menu(bot)

    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    dp.update.outer_middleware(AuthMiddleware())
    dp.update.outer_middleware(ReminderServiceMiddleware())

    try:
        asyncio.create_task(amqp_consume_queue(bot))
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except Exception:
        log.error("Something went wrong", exc_info=True)


if __name__ == "__main__":
    asyncio.run(main())
