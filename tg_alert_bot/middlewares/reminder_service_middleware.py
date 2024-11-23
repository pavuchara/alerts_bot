from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User

from services.backend.exceptions import AuthUserException
from services.backend.reminder_service import ReminderService


class ReminderServiceMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ):
        user_token: User = data.get("user_backend_token")
        if not user_token:
            raise AuthUserException("Что-то не так с бекендом, попробуй попозже")

        reminder_service = ReminderService(user_token=user_token)
        data["reminder_service"] = reminder_service
        result = await handler(event, data)
        return result
