from celery import Celery # type: ignore
from celery.schedules import crontab # type: ignore

import config
from reminder.tasks import alert_notification


celery = Celery(
    __name__,
    broker=config.CELERY_BACKEND,
    backend=config.CELERY_BACKEND,
    broker_connection_retry_on_startup=True,
)


celery.conf.beat_schedule = {
    "alert_notification": {
        "task": "reminder.tasks.alert_notification",
        "schedule": crontab(),
    }
}

# celery -A celery_config:celery worker --beat --loglevel=info
