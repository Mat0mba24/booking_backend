from celery import Celery
from celery.schedules import crontab

from app.config import settings

celery = Celery(
    "tasks",
    broker=f"redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}",
    include=[
        "app.tasks.tasks",
        "app.tasks.scheduled",
    ]
)

# Расписание запуска задач для celery beat
# Ключ в словаре может быть любым, а внутри "task": <value> value должно быть названием таски 
celery.conf.beat_schedule = {
    "email.booking_reminder_1day": {
        "task": "email.booking_reminder_1day",
        "schedule": crontab(minute="0", hour="9"),  # каждое утро в 9:00
    },
    "email.booking_reminder_3days": {
        "task": "email.booking_reminder_3days",
        "schedule": crontab(minute="0", hour="13"),  # каждый день в 13:00
    },
    "luboe-nazvanie": {
        "task": "periodic_task",
        "schedule": 60 * 5,  # секунды
        # "schedule": crontab(hour="15", minute="30"),
    }
}
