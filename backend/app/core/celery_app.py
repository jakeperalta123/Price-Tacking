from celery import Celery
from celery.schedules import crontab

celery_app = Celery(
    "worker", 
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

