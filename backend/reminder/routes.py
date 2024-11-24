from typing import Annotated, Any

from fastapi import (
    APIRouter,
    HTTPException,
    status,
    Depends,
    Path,
)

from auth.dependencies import get_current_user
from reminder.dependencies import get_reminder_service
from reminder.exceptions import (
    ReminderDoesNotExistException,
    ReminderLimitException,
    ReminderPermissionsException,
)
from reminder.services import ReminderService
from reminder.schemas import (
    ReminderRetriveSchema,
    ReminderCreateSchema,
    ReminderUpdateSchema,
)


router = APIRouter(prefix="/reminders", tags=["Reminders"])


@router.get(
    "/",
    response_model=list[ReminderRetriveSchema],
    status_code=status.HTTP_200_OK,
)
async def get_all_reminders(
    reminder_service: Annotated[ReminderService, Depends(get_reminder_service)],
    current_user: Annotated[dict[str, Any], Depends(get_current_user)],
):
    if current_user["is_admin"]:
        return await reminder_service.get_all_reminders()
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Forbidden",
    )


@router.post(
    "/",
    response_model=ReminderRetriveSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_reminder(
    reminder_data: ReminderCreateSchema,
    reminder_service: Annotated[ReminderService, Depends(get_reminder_service)],
    current_user: Annotated[dict[str, Any], Depends(get_current_user)],
):
    try:
        return await reminder_service.create_reminder(
            reminder_data=reminder_data,
            user_id=current_user["id"]
        )
    except ReminderLimitException as e:
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail=str(e),
        )


@router.get(
    "/my_reminders",
    response_model=list[ReminderRetriveSchema],
    status_code=status.HTTP_200_OK,
)
async def get_user_reminders(
    reminder_service: Annotated[ReminderService, Depends(get_reminder_service)],
    current_user: Annotated[dict[str, Any], Depends(get_current_user)],
):
    return await reminder_service.get_reminders_by_user_id(
        user_id=current_user["id"]
    )


@router.get(
    "/{reminder_id}",
    response_model=ReminderRetriveSchema,
    status_code=status.HTTP_200_OK,
)
async def get_reminder_by_id(
    reminder_id: Annotated[int, Path(ge=1)],
    reminder_service: Annotated[ReminderService, Depends(get_reminder_service)],
    current_user: Annotated[dict[str, Any], Depends(get_current_user)],
):
    try:
        return await reminder_service.get_reminder_by_id(
            reminder_id=reminder_id,
            user_id=current_user["id"]
        )
    except ReminderDoesNotExistException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.put(
    "/{reminder_id}",
    response_model=ReminderRetriveSchema,
    status_code=status.HTTP_200_OK,
)
async def update_reminder(
    reminder_id: Annotated[int, Path(ge=1)],
    reminder_data: ReminderUpdateSchema,
    reminder_service: Annotated[ReminderService, Depends(get_reminder_service)],
    current_user: Annotated[dict[str, Any], Depends(get_current_user)],
):
    try:
        return await reminder_service.update_reminder(
            user_id=current_user["id"],
            reminder_id=reminder_id,
            reminder_data=reminder_data,
        )
    except ReminderDoesNotExistException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except ReminderPermissionsException as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )


@router.delete(
    "/{reminder_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_reminder(
    reminder_id: Annotated[int, Path(ge=1)],
    reminder_service: Annotated[ReminderService, Depends(get_reminder_service)],
    current_user: Annotated[dict[str, Any], Depends(get_current_user)],
):
    try:
        return await reminder_service.delete_reminder(
            user_id=current_user["id"],
            reminder_id=reminder_id,
        )
    except ReminderDoesNotExistException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except ReminderPermissionsException as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )
