from celery import Celery # type: ignore
from celery.schedules import crontab # type: ignore

import config
from reminder.tasks import schedule_notification_queue_sender


celery = Celery(
    __name__,
    broker=config.CELERY_BACKEND,
    backend=config.CELERY_BACKEND,
    broker_connection_retry_on_startup=True,
)


celery.conf.beat_schedule = {
    "schedule_notification_queue_sender": {
        "task": "reminder.tasks.schedule_notification_queue_sender",
        "schedule": crontab(),
    }
}
