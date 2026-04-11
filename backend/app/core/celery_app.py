from celery import Celery
from celery.schedules import crontab

celery_app = Celery(
    "worker", 
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

celery_app.conf.beat_schedule = {
    'daily-walmart-scrape-at-noon': {
        'task': 'daily_noon_check', 
        'schedule': crontab(minute='*'),
    },
}

celery_app.conf.timezone = 'America/New_York'
celery_app.conf.enable_utc = True
import app.tasks.scraper_tasks
celery_app.autodiscover_tasks(['app.tasks'])