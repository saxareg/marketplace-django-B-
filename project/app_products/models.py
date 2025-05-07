from django.db import models
from app_shops.models import Shop
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Product(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/', default='products/default-preview.jpg', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['shop', 'category', 'is_active']),
            models.Index(fields=['price', 'created_at']),
        ]


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)], db_index=True)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"Review for {self.product.name} by {self.user.username}"

    class Meta:
        indexes = [models.Index(fields=['product', 'user'])]
