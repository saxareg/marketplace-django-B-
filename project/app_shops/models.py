from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Shop(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Название магазина
    slug = models.SlugField(max_length=100, unique=True)  # SEO-дружественный URL
    description = models.TextField(blank=True, null=True)  # Описание магазина
    logo = models.ImageField(upload_to='shops/', default='shops/default_shop_logo.jpg', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)  # Время создания
    is_active = models.BooleanField(default=True, db_index=True)  # Активность магазина
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shops')  # Владелец

    def __str__(self):
        return self.name

    class Meta:
        indexes = [models.Index(fields=['owner', 'is_active'])]


class ShopCreationRequest(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Название магазина
    slug = models.SlugField(max_length=100, unique=True)  # SEO-дружественный URL
    description = models.TextField(blank=True, null=True)  # Описание магазина
    logo = models.ImageField(upload_to='shops/', default='shops/default_shop_logo.jpg', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)  # Время создания
    is_active = models.BooleanField(default=True, db_index=True)  # Активность заявки
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Пользователь, отправивший заявку
    status = models.CharField(max_length=10, choices=[
        ('pending', 'В обработке'),
        ('approved', 'Одобрена'),
        ('rejected', 'Отклонена')
    ], default='pending')
    response_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Заявка на создание магазина: {self.name} от {self.user.username}"
