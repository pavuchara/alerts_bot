from typing import Annotated, Any

from fastapi import (
    HTTPException,
    status,
    Depends,
)
from fastapi.security import OAuth2PasswordBearer

from auth.exceptions import AuthUserException
from auth.services import AuthJWTService
from users.dependencies import get_user_repository
from users.repositories import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


async def get_auth_service(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)]
) -> AuthJWTService:
    return AuthJWTService(user_repository=user_repository)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    auth_service: Annotated[AuthJWTService, Depends(get_auth_service)],
) -> dict[str, Any]:
    try:
        return await auth_service.decode_token(token=token)
    except AuthUserException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )
