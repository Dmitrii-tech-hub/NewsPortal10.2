from celery import Celery
from celery.schedules import crontab
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_portal.settings')

app = Celery('news_portal')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send-weekly-posts': {
        'task': 'simpleapp.tasks.send_weekly_posts',
        'schedule': crontab(day_of_week=1, hour=8, minute=0),  # Every Monday at 8:00 AM
    },
}

