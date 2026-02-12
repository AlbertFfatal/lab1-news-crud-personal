from celery import Celery
from celery.schedules import crontab
# Graceful shutdown работает по умолчанию в Celery
celery = Celery(
    "tasks",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
    include=["app.tasks"]
)

celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    beat_schedule={
        "weekly-digest": {
            "task": "app.tasks.weekly_digest_task",
            "schedule": crontab(day_of_week=0, hour=12, minute=0),  # воскресенье 12:00
        }
    },
    task_acks_late=True,
    worker_prefetch_multiplier=1,
)