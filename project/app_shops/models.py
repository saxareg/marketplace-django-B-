from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class BaseShop(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Название магазина
    slug = models.SlugField(max_length=100, unique=True)  # SEO-дружественный URL
    description = models.TextField(blank=True, null=True)  # Описание магазина
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shops', null=True, blank=True)  # Владелец
    logo = models.ImageField(upload_to='shops/logos/', default='shops/logos/default.jpg', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)  # Время создания
    is_active = models.BooleanField(default=True, db_index=True)  # Активность магазина

    class Meta:
        abstract = True


class Shop(BaseShop):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shops')  # Владелец для Shop

    def __str__(self):
        return self.name

    class Meta:
        indexes = [models.Index(fields=['owner', 'is_active'])]


class ShopCreationRequest(BaseShop):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Владелец для ShopCreationRequest
    status = models.CharField(max_length=10,
                              choices=[('pending', 'В обработке'),
                                       ('approved', 'Одобрена'),
                                       ('rejected', 'Отклонена')], default='pending')
    response_time = models.DateTimeField(null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests')

    def __str__(self):
        return f"Заявка на создание магазина: {self.name} от {self.user.username}"
