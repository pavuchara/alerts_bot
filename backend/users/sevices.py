from abc import ABC, abstractmethod
from typing import Sequence

from users.exceptions import UserDoesNotExistException
from users.models import User
from users.repositories import UserRepository
from users.utils import RegistationSource
from users.schemas import (
    UserCreateSchema,
    UserUpdateSchema,
)


class AbstractUserService(ABC):

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
    async def update_user(self, user_id: int, user_data: UserUpdateSchema) -> User:
        raise NotImplementedError


class UserService(AbstractUserService):

    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    async def get_all_users(self) -> Sequence[User]:
        users = await self.user_repository.get_all_users()
        return users

    async def get_user_by_id(self, user_id: int, raise_exc: bool = True) -> User | None:
        user = await self.user_repository.get_user_by_id(user_id=user_id)
        if raise_exc and not user:
            raise UserDoesNotExistException()
        return user

    async def get_user_by_email(self, user_email: str, raise_exc: bool = True) -> User | None:
        user = await self.user_repository.get_user_by_email(user_email=user_email)
        if raise_exc and not user:
            raise UserDoesNotExistException()
        return user

    async def get_user_by_tg_id(self, tg_id: int, raise_exc: bool = True) -> User | None:
        user = await self.user_repository.get_user_by_tg_id(tg_id=tg_id)
        if raise_exc and not user:
            raise UserDoesNotExistException()
        return user

    async def create_user(
        self,
        user_data: UserCreateSchema,
        registration_source: str = RegistationSource.manual.value
    ) -> User:
        user = await self.user_repository.create_user(
            user_data=user_data,
            registration_source=registration_source,
        )
        return user

    async def update_user(self, user_id: int, user_data: UserUpdateSchema) -> User:
        user = await self.user_repository.update_user(
            user_id=user_id,
            user_data=user_data,
        )
        return user
