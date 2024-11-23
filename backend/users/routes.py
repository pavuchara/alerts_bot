from typing import Annotated, Any

from fastapi import (
    APIRouter,
    HTTPException,
    status,
    Depends,
    Path,
)
from sqlalchemy.exc import IntegrityError

from auth.dependencies import get_current_user
from users.dependencies import get_user_service
from users.sevices import UserService
from users.schemas import (
    UserRetrieveSchema,
    UserCreateSchema,
    UserUpdateSchema,
)
from users.exceptions import UserDoesNotExistException


router = APIRouter(prefix="/users", tags=["user"])


@router.get("/", response_model=list[UserRetrieveSchema], status_code=status.HTTP_200_OK)
async def get_all_users(
    user_service: Annotated[UserService, Depends(get_user_service)],
    current_user: Annotated[dict[str, Any], Depends(get_current_user)],
):
    if current_user["is_admin"]:
        return await user_service.get_all_users()
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Forbidden",
    )


@router.post("/", response_model=UserRetrieveSchema, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreateSchema,
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    try:
        return await user_service.create_user(user_data=user_data)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User alredy exists",
        )


@router.get("/{user_id}", response_model=UserRetrieveSchema, status_code=status.HTTP_200_OK)
async def get_user_by_id(
    user_id: Annotated[int, Path()],
    user_service: Annotated[UserService, Depends(get_user_service)],
    current_user: Annotated[dict[str, Any], Depends(get_current_user)],
):
    try:
        if current_user["is_admin"] or current_user["id"] == user_id:
            return await user_service.get_user_by_id(user_id=user_id)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden",
        )
    except UserDoesNotExistException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.put("/{user_id}", response_model=UserRetrieveSchema, status_code=status.HTTP_200_OK)
async def update_user(
    user_data: UserUpdateSchema,
    user_id: Annotated[int, Path()],
    current_user: Annotated[dict[str, Any], Depends(get_current_user)],
    user_service: Annotated[UserService, Depends(get_user_service)],

):
    if current_user["id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only owner can update this profile",
        )

    try:
        return await user_service.update_user(user_id=user_id, user_data=user_data)
    except UserDoesNotExistException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
