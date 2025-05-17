from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from app_users.models import UserProfile
import os


class Command(BaseCommand):
    help = 'Создание суперпользователя и профиля, если они ещё не существуют'

    def handle(self, *args, **options):
        User = get_user_model()
        username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin')
        email = os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@domain.com')
        password = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'admin')

        user, created = User.objects.get_or_create(username=username, defaults={'email': email})
        if created:
            user.set_password(password)
            user.is_superuser = True
            user.is_staff = True
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Суперпользователь "{username}" создан.'))
        else:
            self.stdout.write(self.style.WARNING(f'Суперпользователь "{username}" уже существует.'))

        if not UserProfile.objects.filter(user=user).exists():
            UserProfile.objects.create(user=user, role='admin')
            self.stdout.write(self.style.SUCCESS(f'Профиль для суперпользователя "{username}" создан.'))
        else:
            self.stdout.write(self.style.WARNING(f'Профиль для суперпользователя "{username}" уже существует.'))

