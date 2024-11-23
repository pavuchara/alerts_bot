from datetime import (
    datetime,
    timezone,
)
from typing import Any

from aiohttp import ClientResponse, ClientSession
from jose import (
    jwt,
    JWTError,
    ExpiredSignatureError,
)
from aiogram.types import User

from config import (
    API_KEY,
    ACCESS_TOKEN_LIFETIME,
    ALGORITHM,
)
from services.connectors import get_session
from services.backend.domen import BackendPaths
from services.backend.exceptions import (
    AuthUserException,
    TokenExpireException,
)


class AuthService:
    def __init__(self, user: User) -> None:
        self.user = user

    async def authenticate_user(self) -> str:
        """
            Authenticates the user.
            If not, registers, then repeats the request.
        """
        async with get_session() as session:
            user_token: str = await self.__create_access_token_for_remote_service()
            headers = {"Authorization": f"Bearer {user_token}"}

            response = await self.__make_auth_request(session, headers)
            response_data = await response.json()
            if response.status == 400 and response_data.get("detail") == "User does not exists.":
                #  if user is newbe, process registration:
                await self.__registrate_user(session)
                response = await self.__make_auth_request(session, headers)

            await self._raise_for_status(response, 200)
            response_data = await response.json()
            await self.__decode_remote_response_token(response_data.get("access_token"))

            return response_data.get("access_token")

    async def __decode_remote_response_token(self, token: str) -> Any:
        try:
            jwt.decode(token, API_KEY, algorithms=ALGORITHM)
        except ExpiredSignatureError:
            raise TokenExpireException()
        except JWTError:
            raise AuthUserException("Invalid token")

    async def __create_access_token_for_remote_service(self) -> str:
        encode = {"tg_id": self.user.id, "exp": datetime.now(timezone.utc) + ACCESS_TOKEN_LIFETIME}
        return jwt.encode(encode, API_KEY, algorithm=ALGORITHM)

    async def __registrate_user(self, session: ClientSession) -> None:
        payload_data = {
            "email": None,
            "password": None,
            "telegram_id": self.user.id,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
        }
        async with session.post(BackendPaths.USERS.value, json=payload_data) as response:
            await self._raise_for_status(response, 201)

    async def __make_auth_request(
        self,
        session: ClientSession,
        headers: dict[str, str]
    ) -> ClientResponse:
        """Sends an authentication request."""
        return await session.post(BackendPaths.TOKEN.value, headers=headers)

    @staticmethod
    async def _raise_for_status(response: ClientResponse, expected_status: int) -> None:
        """Raises exception for status."""
        if response.status != expected_status:
            raise AuthUserException(f"Unexpected response: {response.status}")
