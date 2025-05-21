from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    Model representing additional profile information for a User.
    Attributes:
        user (OneToOneField): One-to-one relationship with Django's User model.
        phone (CharField): User's phone number.
        role (CharField): Role of the user in the system (buyer, seller, admin, pickup point staff).
        pickup_point (ForeignKey): Reference to the PickupPoints where the user works (if staff).
        created_at (DateTimeField): Timestamp when the profile was created.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=20, choices=[
        ('buyer', 'Покупатель'),
        ('seller', 'Продавец'),
        ('admin', 'Администратор'),
        ('pp_staff', 'Сотрудник ПВЗ'),
    ], default='buyer', db_index=True)
    pickup_point = models.ForeignKey('PickupPoints',
                                     on_delete=models.SET_NULL,
                                     null=True, blank=True,
                                     related_name='staff')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

    class Meta:
        indexes = [models.Index(fields=['user', 'role'])]


class PickupPoints(models.Model):
    """
    Model representing pickup points for order collection.
    Attributes:
        name (CharField): Name of the pickup point.
        city (CharField): City where the pickup point is located.
        street (CharField): Street address of the pickup point.
        postal_code (CharField): Postal code of the pickup point location.
        description (TextField): Additional description or notes.
        is_active (BooleanField): Status indicating whether the pickup point is active.
    """

    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100, db_index=True)
    street = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        indexes = [models.Index(fields=['city', 'is_active'])]
        verbose_name = 'Pickup Point'
        verbose_name_plural = 'Pickup Points'
