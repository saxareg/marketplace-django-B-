from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'mark_unclaimed_orders_every_day': {
        'task': 'app_orders.tasks.mark_unclaimed_orders',
        'schedule': crontab(minute=0, hour=0),  # каждый день в 00:00
    },
}
