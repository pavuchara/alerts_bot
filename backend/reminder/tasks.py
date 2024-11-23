import logging
from datetime import datetime
from typing import Any

import pytz
from celery import shared_task  # type: ignore
from sqlalchemy import select

from database.db import sync_session_maker
from users.models import User
from reminder.models import Reminder
from remote_services.dependencies import sync_get_telegram_pusher_service

log = logging.getLogger(__name__)


@shared_task
def schedule_notification_queue_sender() -> None:
    with sync_session_maker() as db:
        try:
            reminders = list(
                db.scalars(
                    select(Reminder)
                    .join(User)
                    .filter(User.telegram_id.is_not(None))
                    .where(
                        Reminder.alert_datetime < datetime.now(pytz.timezone("Europe/Moscow")),
                    )
                ).all()
            )
            messages: list[dict[str, Any]] = []
            for reminder in reminders:
                messages.append({
                    "tg_id": reminder.author.telegram_id,
                    "description": reminder.description,
                    "alert_datetime": reminder.alert_datetime,
                })
            if messages:
                tg_service = sync_get_telegram_pusher_service()
                tg_service.push_messages(messages=messages)

            for reminder in reminders:
                db.delete(reminder)
                db.commit()
                log.warning("DELETE REMINDER" * 5)

            log.info("send messages to queue")
        except Exception:
            db.rollback()
            log.error("messages not sended", exc_info=True)
            raise
        finally:
            db.close()
