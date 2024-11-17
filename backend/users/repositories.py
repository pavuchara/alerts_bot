from abc import ABC, abstractmethod
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from passlib.context import CryptContext
from users.exceptions import UserDoesNotExistException
from users.models import User
from users.schemas import (
    UserCreateSchema,
    UserUpdateSchema,
)

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AbstractUserRepository(ABC):

    @abstractmethod
    async def get_all_users(self) -> Sequence[User]:
        raise NotImplementedError

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def get_user_by_email(self, email: str) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def get_user_by_tg_id(self, tg_id: int) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def create_user(self, user_data: UserCreateSchema, registration_source: str) -> User:
        raise NotImplementedError

    @abstractmethod
    async def update_user(self, user_id: int, user_data: UserUpdateSchema) -> User | None:
        raise NotImplementedError


class UserRepository(AbstractUserRepository):

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_all_users(self) -> Sequence[User]:
        users = await self.db.scalars(select(User))
        return users.all()

    async def get_user_by_id(self, user_id: int) -> User | None:
        user = await self.db.scalar(
            select(User)
            .where(User.id == user_id)
        )
        return user

    async def get_user_by_email(self, user_email: str) -> User | None:
        user = await self.db.scalar(
            select(User)
            .where(User.email == user_email)
        )
        return user

    async def get_user_by_tg_id(self, tg_id: int) -> User | None:
        user = await self.db.scalar(
            select(User)
            .where(User.telegram_id == tg_id)
        )
        return user

    async def create_user(self, user_data: UserCreateSchema, registration_source: str) -> User:
        user_password = user_data.password
        if user_data.password is not None:
            user_password = bcrypt_context.hash(user_data.password)
        user = User(
            email=user_data.email,
            password=user_password,
            telegram_id=user_data.telegram_id,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            registration_source=registration_source,
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def update_user(self, user_id: int, user_data: UserUpdateSchema) -> User:
        user = await self.get_user_by_id(user_id=user_id)
        if user:
            user.first_name = user_data.first_name
            user.last_name = user_data.last_name
            self.db.add(user)
            await self.db.commit()
            return user
        raise UserDoesNotExistException()
