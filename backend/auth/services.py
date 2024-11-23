from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Any

from jose import (
    jwt,
    JWTError,
    ExpiredSignatureError,
)
from passlib.context import CryptContext

from config import (
    API_KEY,
    ALGORITHM,
    ACCESS_TOKEN_LIFETIME,
)
from auth.exceptions import AuthUserException
from users.models import User
from users.repositories import UserRepository


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AbstractAuthJWTService(ABC):

    @abstractmethod
    async def authenticate_manual_user(self, email: str, password: str) -> User:
        raise NotImplementedError

    @abstractmethod
    async def authenticate_tg_user(self, token_from_tg: str) -> User:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    async def create_access_token(user: User):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    async def decode_token(token: str) -> dict[str, Any]:
        raise NotImplementedError


class AuthJWTService(AbstractAuthJWTService):

    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    async def authenticate_manual_user(self, email: str, password: str) -> User:
        user = await self.user_repository.get_user_by_email(email)
        if not user or (user and not bcrypt_context.verify(password, user.password)):
            raise AuthUserException()
        return user

    async def authenticate_tg_user(self, token_from_tg: str) -> User:
        try:
            user_info = jwt.decode(token_from_tg, API_KEY, algorithms=ALGORITHM)
            user = await self.user_repository.get_user_by_tg_id(user_info["tg_id"])
            if user is None:
                raise AuthUserException("User does not exists.")
        except KeyError:
            raise AuthUserException("Invalid token.")
        except ExpiredSignatureError:
            raise AuthUserException("Token expired.")
        except JWTError as e:
            raise AuthUserException(str(e))
        else:
            return user

    @staticmethod
    async def create_access_token(user: User) -> str:
        encode = {
            "id": user.id,
            "email": user.email,
            "telegram_id": user.telegram_id,
            "is_admin": user.is_admin,
        }
        expires = datetime.now(timezone.utc) + ACCESS_TOKEN_LIFETIME
        encode.update({"exp": expires})
        return jwt.encode(encode, API_KEY, algorithm=ALGORITHM)

    @staticmethod
    async def decode_token(token: str) -> dict[str, Any]:
        try:
            return jwt.decode(token, API_KEY, algorithms=ALGORITHM)
        except ExpiredSignatureError:
            raise AuthUserException("Token expired")
        except JWTError:
            raise AuthUserException()
