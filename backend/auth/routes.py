from typing import Annotated

from fastapi import (
    APIRouter,
    Request,
    HTTPException,
    status,
    Depends,
)
from fastapi.security import OAuth2PasswordRequestForm

from auth.dependencies import get_auth_service
from auth.exceptions import AuthUserException
from auth.services import AuthJWTService
from auth.schemas import AccessTokenSchema


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/token", response_model=AccessTokenSchema, status_code=status.HTTP_200_OK)
async def get_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: Annotated[AuthJWTService, Depends(get_auth_service)],
):
    try:
        user = await auth_service.authenticate_manual_user(
            email=form_data.username,
            password=form_data.password,
        )
        access_token = await auth_service.create_access_token(user=user)
        return {
            "access_token": access_token,
            "token_type": "bearer",
        }
    except AuthUserException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post("/tg_user_token", response_model=AccessTokenSchema, status_code=status.HTTP_200_OK)
async def get_access_token_for_tg_user(
    request: Request,
    auth_service: Annotated[AuthJWTService, Depends(get_auth_service)],
):
    token_from_tg = request.headers.get("Authorization")
    if token_from_tg is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Out of token.",
        )
    try:
        user = await auth_service.authenticate_tg_user(token_from_tg=token_from_tg)
        access_token = await auth_service.create_access_token(user=user)
        return {
            "access_token": access_token,
            "token_type": "bearer",
        }
    except AuthUserException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
