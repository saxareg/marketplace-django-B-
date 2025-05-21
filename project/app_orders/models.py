from django.db import models
from django.contrib.auth.models import User
from app_products.models import Product
from app_users.models import PickupPoints
from app_shops.models import Shop


class Cart(models.Model):
    """Represents a shopping cart associated with a single user."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"Cart of {self.user.username}"


class CartItem(models.Model):
    """Represents a product and its quantity in a user's cart."""

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    class Meta:
        indexes = [models.Index(fields=['cart', 'product'])]


class Order(models.Model):
    """
    Represents a finalized order created from the shopping cart.
    Includes references to the user, the shop, and the pickup point.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='orders')
    pickup_point = models.ForeignKey(PickupPoints, on_delete=models.SET_NULL, null=True, related_name='orders')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('confirmed', 'Confirmed'),
            ('shipped', 'В пути'),
            ('ready_for_pickup', 'Готов к выдаче'),
            ('delivered', 'Доставлен'),
            ('returned', 'Возвращен'),
            ('unclaimed', 'Просрочен'),
        ],
        default='shipped',
        db_index=True
    )
    is_paid = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    status_updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

    class Meta:
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['shop', 'status']),
            models.Index(fields=['status_updated_at']),
        ]


class OrderItem(models.Model):
    """Represents a product included in a specific order with its quantity and price."""

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order #{self.order.id}"

    class Meta:
        indexes = [models.Index(fields=['order', 'product'])]
