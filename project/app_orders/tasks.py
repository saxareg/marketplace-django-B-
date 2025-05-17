from celery import shared_task
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from .models import Order


@shared_task
def notify_ready_order(order_id, username, email, pickup_point):
    """
    Sends an email notification to the user when their order is ready for pickup.
    Args:
        order_id (int): The ID of the order.
        username (str): The username of the customer.
        email (str): The email address of the customer.
        pickup_point (str): The name of the pickup point."""

    order = Order.objects.get(pk=order_id)

    send_mail(
        subject='Your order is ready for pickup',
        message=(
            f'Hello, {username}!\n\n'
            f'Your order #{order.id} is now ready for pickup at "{pickup_point}".\n'
            f'Thank you for shopping with us!\n\n'
            'Best regards,\nThe Marketplace Team'
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )


@shared_task
def mark_unclaimed_orders():
    """
    Checks for orders that have been ready for pickup for over 7 days and
    marks them as 'unclaimed'. Sends an email notification to the user.
    """

    # Find orders that have not been picked up within 7 days
    seven_days_ago = timezone.now() - timedelta(days=7)
    orders = Order.objects.filter(
        status='ready_for_pickup',
        status_updated_at__lte=seven_days_ago
    )

    for order in orders:
        order.status = 'unclaimed'
        order.save()

        send_mail(
            subject='Order marked as unclaimed',
            message=(
                f'Hello, {order.user.username}.\n'
                f'Your order #{order.id} has been marked as "Unclaimed" due to inactivity.\n\n'
                'Please contact support if you have any questions.\n\n'
                'Best regards,\nThe Marketplace Team'
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[order.user.email],
            fail_silently=False,
        )
    return f"{orders.count()} orders marked unclaimed"
