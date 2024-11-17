from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.db_depends import get_db_session
from users.repositories import UserRepository
from users.sevices import UserService


async def get_user_repository(
    db_sessinon: Annotated[AsyncSession, Depends(get_db_session)]
) -> UserRepository:
    return UserRepository(db=db_sessinon)


async def get_user_service(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)]
) -> UserService:
    return UserService(user_repository=user_repository)
