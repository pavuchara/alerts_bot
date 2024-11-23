from typing import Any
from datetime import datetime

from services.connectors import get_session
from services.backend.domen import BackendPaths
from services.backend.exceptions import ReminderServiceException


class ReminderService:

    def __init__(self, user_token) -> None:
        self.__user_token: str = user_token

    async def create_reminder(self, reminder_data: dict[str, Any]) -> None:
        prepared_data = await self.__prepare_post_data(reminder_data=reminder_data)

        async with get_session() as session:
            async with session.post(
                BackendPaths.REMINDERS.value,
                headers=await self.__get_auth_headers(),
                json=prepared_data,
            ) as response:
                if response.status != 201:
                    raise ReminderServiceException(
                        "Не получилось создать, поробуй снова или попозже. "
                        "Скорее всего в процессе заполнения прошло слишком много времени..."
                    )

    async def get_self_reminders(self) -> list[dict[str, Any]]:
        async with get_session() as session:
            async with session.get(
                BackendPaths.SELF_REMINDERS.value,
                headers=await self.__get_auth_headers(),
            ) as response:
                if response.status != 200:
                    raise ReminderServiceException("Не вышло получить напоминания, попробуй позже")
                response_dct = await response.json()
                return await self.__prepare_response_bot_data(response=response_dct)

    async def delete_reminder_by_id(self, reminder_id: int) -> None:
        path = BackendPaths.REMINDERS.value + str(reminder_id)
        async with get_session() as session:
            async with session.delete(path, headers=await self.__get_auth_headers()) as response:
                if response.status != 204:
                    raise ReminderServiceException(
                        "Не получилось удалить напоминание, попробуй позже"
                    )

    async def __get_auth_headers(self):
        return {
            "Authorization": f"Bearer {self.__user_token}"
        }

    async def __prepare_post_data(
        self,
        reminder_data: dict[str, Any]
    ) -> dict[str, Any]:
        expected_data: dict = {
            "alert_datetime": reminder_data["normalized_datetime"].isoformat(),
            "description": reminder_data["description"]

        }
        return expected_data

    async def __prepare_response_bot_data(
        self,
        response: list[dict[str, Any]] | list
    ) -> list[dict[str, Any]]:
        if not response:
            return response
        response.sort(key=lambda x: x["alert_datetime"])

        result_reminders: list[dict] = []
        for reminder in response:
            message_date = (
                datetime
                .fromisoformat(reminder["alert_datetime"])
                .strftime("%d.%m.%Y %H:%M")
            )
            reminder_data = {
                "message": f"{message_date} - {reminder["description"]}"[:60],
                "reminder_id": str(reminder["id"]),
            }
            result_reminders.append(reminder_data)
        return result_reminders
