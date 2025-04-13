from django.db import models
from django.contrib.auth.models import User

# Create your models here.

"""
Назначение: Управление магазинами.
Типичные запросы:
* Поиск магазина по slug или владельцу.
* Фильтрация активных магазинов.
"""

class Shop(models.Model):
    """
    Описание полеей
    * name и slug: Уникальные поля для названия и URL магазина.
    * description: Для описания магазина (опционально).
    * owner: Связь с User (продавцом), чтобы указать владельца.
    * logo: Для загрузки изображения магазина (опционально, требуется Pillow).
    * is_active: Для модерации (например, отключение магазина админом).
    Зависимость от app_users через User.
    """
    name = models.CharField(max_length=100, unique=True)  # Уникальность создаёт индекс
    slug = models.SlugField(max_length=100, unique=True)  # Уникальность создаёт индекс
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shops')
    logo = models.ImageField(upload_to='shops/logos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)  # Индекс для сортировки
    is_active = models.BooleanField(default=True, db_index=True)  # Индекс для фильтрации

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['owner', 'is_active']),  # Составной индекс для поиска активных магазинов владельца
        ]
