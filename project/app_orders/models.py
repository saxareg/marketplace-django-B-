from django.db import models
from django.contrib.auth.models import User
from app_products.models import Product
from app_users.models import PickupPoints
from app_shops.models import Shop
# Create your models here.

"""
Назначение: Управление корзиной и заказами.
Модели:
* Cart: Корзина пользователя.
* CartItem: Элементы корзины.
* Order: Заказы.
* OrderItem: Элементы заказа.
Зависимости: Product из app_products, Address из app_users, Shop из app_shops.
"""

class Cart(models.Model):
    """
    OneToOneField с User для уникальной корзины.
    Для анонимных пользователей корзину можно хранить в сессиях (логика в views.py).
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)  # Индекс для сортировки

    def __str__(self):
        return f"Cart of {self.user.username}"


class CartItem(models.Model):
    """
    Связь с Cart и Product.
    quantity для указания количества товара.
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    class Meta:
        indexes = [
            models.Index(fields=['cart', 'product']),  # Составной индекс для поиска элементов корзины
        ]

class Order(models.Model):
    """
    Связь с User, Shop, и Address.
    total_price для итоговой суммы.
    status с базовыми состояниями заказа.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='orders')
    pickup_point = models.ForeignKey(PickupPoints, on_delete=models.SET_NULL, null=True, related_name='orders')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)  # Индекс для фильтрации
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Ожидает'),
            ('confirmed', 'Подтверждён'),
            ('shipped', 'Отправлен'),
            ('delivered', 'Доставлен'),
        ],
        default='pending',
        db_index=True  # Индекс для фильтрации
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)  # Индекс для сортировки

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

    class Meta:
        indexes = [
            models.Index(fields=['user', 'status']),  # Составной индекс для фильтрации заказов пользователя
            models.Index(fields=['shop', 'status']),  # Составной индекс для фильтрации заказов магазина
        ]

class OrderItem(models.Model):
    """
    Хранит товары заказа с их ценой на момент покупки (чтобы цена не менялась, если товар подорожал).
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order #{self.order.id}"

    class Meta:
        indexes = [
            models.Index(fields=['order', 'product']),  # Составной индекс для поиска элементов заказа
        ]
