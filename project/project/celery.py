from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    """Debug task to test Celery setup.
    Prints the request information for the current task.
    Args:
        self: Task instance, automatically passed when bind=True.
    """

    print(f'Request: {self.request!r}')


CELERY_BEAT_SCHEDULE = {
    'mark_unclaimed_orders_every_day': {
        'task': 'app_orders.tasks.mark_unclaimed_orders',
        'schedule': crontab(minute=0, hour=0),
        # This schedule runs the task daily at midnight (00:00).
    },
}
