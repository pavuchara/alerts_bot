from datetime import datetime

import pytz
from celery import shared_task  # type: ignore
from sqlalchemy import select

from users.models import User
from reminder.models import Reminder

from database.db import sync_session_maker


@shared_task
def alert_notification():
    with sync_session_maker() as db:
        try:
            reminders = db.scalars(
                select(Reminder)
                .join(User)
                .filter(User.telegram_id is not None)
                .where(
                    Reminder.alert_datetime < datetime.now(pytz.timezone("Europe/Moscow")),
                )
            )
            for reminder in reminders.all():
                # TODO realize
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()
