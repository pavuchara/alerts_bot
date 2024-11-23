from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User

from services.backend.auth import AuthService
from services.backend.exceptions import (
    TokenExpireException,
    AuthUserException,
)


class AuthMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ):
        user: User = data.get("event_from_user")

        if not user:
            raise ValueError()  # TODO SODKSODKOSDOKWS

        service = AuthService(user)

        # TODO CACHE
        try:
            user_token: dict[str, Any] = await service.authenticate_user()
        except TokenExpireException:
            user_token: dict[str, Any] = await service.authenticate_user()
        except AuthUserException:
            pass   # TODO SODKSODKOSDOKWS

        data["user_backend_token"] = user_token
        result = await handler(event, data)
        return result
