from django.db import models
from ..app_shops.models import Shop
from django.contrib.auth.models import User

# Create your models here.

"""
Назначение: Управление товарами и отзывами.
Модели:
* Category: Категории товаров.
* Product: Товары.
* Review: Отзывы на товары.

Типичные запросы:
* Поиск товаров по магазину, категории, slug.
* Фильтрация активных товаров или по цене.
* Получение отзывов по товару или пользователю.

Зависимости: Shop из app_shops, User из app_users.
"""

class Category(models.Model):
    """
    Модель для категоризации товаров.
    slug для SEO-дружественных URL.
    """    
    name = models.CharField(max_length=100, unique=True)  # Уникальность создаёт индекс
    slug = models.SlugField(max_length=100, unique=True)  # Уникальность создаёт индекс

    def __str__(self):
        return self.name

class Product(models.Model):
    """
    Связь с Shop через ForeignKey.
    category с SET_NULL для сохранения товаров при удалении категории.
    price использует DecimalField для точности.
    stock для отслеживания остатков (кол-ва товаров)
    is_active для скрытия товаров (например, при модерации).
    """
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)  # Уникальность создаёт индекс
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)  # Индекс для фильтрации
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)  # Индекс для сортировки
    is_active = models.BooleanField(default=True, db_index=True)  # Индекс для фильтрации

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['shop', 'category', 'is_active']),  # Составной индекс для фильтрации товаров
            models.Index(fields=['price', 'created_at']),  # Составной индекс для сортировки
        ]

class Review(models.Model):
    """
    Связь с Product и User.
    rating — оценка от 1 до 5.
    comment — опциональный текстовый отзыв.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)], db_index=True)  # Индекс для фильтрации
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)  # Индекс для сортировки

    def __str__(self):
        return f"Review for {self.product.name} by {self.user.username}"

    class Meta:
        indexes = [
            models.Index(fields=['product', 'user']),  # Составной индекс для уникальности и поиска
        ]
