from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User

from services.connectors import get_cache_session
from services.backend.auth import AuthService
from services.backend.exceptions import TokenExpireException


class AuthMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ):
        user: User = data.get("event_from_user")
        service = AuthService(user)

        cache_key = f"{user.id}_backend_auth_token"

        async with get_cache_session() as cache:
            user_token = await cache.get(cache_key)
            if not user_token:
                try:
                    user_token: dict[str, Any] = await service.authenticate_user()
                except TokenExpireException:
                    user_token: dict[str, Any] = await service.authenticate_user()
                finally:
                    await cache.set(name=cache_key, value=user_token, ex=60*25)

        data["user_backend_token"] = user_token
        result = await handler(event, data)
        return result
