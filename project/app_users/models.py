from django.db import models
from django.contrib.auth.models import User

# Create your models here.

"""
Назначение: Управление пользователями и адресами.
Типичные запросы:
* Поиск профиля по пользователю.
* Фильтрация адресов по пользователю или is_default.
"""

class UserProfile(models.Model):
    """
    Описание полей:
    * Связь OneToOneField с User для уникального профиля.
    * phone — опциональное поле для контактных данных.
    * role — поле для разделения ролей (покупатель, продавец, администратор). Для простоты используем choices, но можно заменить на Group из Django, если потребуется гибкость.
    * created_at — для отслеживания времени регистрации.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(
        max_length=20,
        choices=[('buyer', 'Покупатель'), ('seller', 'Продавец'), ('admin', 'Администратор')],
        default='buyer',
        db_index=True  # Индекс для фильтрации по ролям
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)  # Индекс для сортировки

    def __str__(self):
        return f"{self.user.username}'s profile"

    class Meta:
        indexes = [
            models.Index(fields=['user', 'role']),  # Составной индекс для поиска профиля по пользователю и роли
        ]

class PickupPoints(models.Model):
    """
    * Поля минимальны: город, улица, почтовый индекс (опционально).
    """
    city = models.CharField(max_length=100, db_index=True)  # Индекс для фильтрации по городу
    street = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    description = models.TextField(blank=True, null=True)  # Поле для описания адреса

    def __str__(self):
        return f"{self.city}, {self.street}"
