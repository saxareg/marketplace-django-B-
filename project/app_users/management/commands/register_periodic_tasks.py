from django.core.management.base import BaseCommand
from django_celery_beat.models import PeriodicTask, CrontabSchedule

class Command(BaseCommand):
    help = 'Registers periodic Celery tasks in the database if not already set.'

    def handle(self, *args, **options):
        # Проверим, существует ли уже задача
        if PeriodicTask.objects.filter(name='mark_unclaimed_orders_every_day').exists():
            self.stdout.write(self.style.WARNING('Periodic task already exists. Skipping.'))
            return

        # Создаём расписание: ежедневно в 00:00
        schedule, _ = CrontabSchedule.objects.get_or_create(
            minute='0',
            hour='0',
            day_of_week='*',
            day_of_month='*',
            month_of_year='*',
            timezone='UTC',
        )

        PeriodicTask.objects.create(
            crontab=schedule,
            name='mark_unclaimed_orders_every_day',
            task='app_orders.tasks.mark_unclaimed_orders',
            enabled=True,
        )

        self.stdout.write(self.style.SUCCESS('Periodic task "mark_unclaimed_orders_every_day" registered successfully.'))
