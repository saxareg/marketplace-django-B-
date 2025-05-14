from celery import shared_task
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from .models import Order


@shared_task
def notify_ready_order(order_id, username, email, pickup_point):

    order = Order.objects.get(pk=order_id)
    send_mail(
        subject='Ваш заказ готов к выдаче',
        message=(
            f'Здравствуйте, {username}!\n\n'
            f'Ваш заказ #{order.id} готов к выдаче в ПВЗ "{pickup_point}".\n'
            f'Спасибо за покупку!\n\n'
            'С уважением,\nКоманда Marketplace'
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )


@shared_task
def mark_unclaimed_orders():
    seven_days_ago = timezone.now() - timedelta(days=7)
    orders = Order.objects.filter(
        status='ready_for_pickup',
        status_updated_at__lte=seven_days_ago
    )
    for order in orders:
        order.status = 'unclaimed'
        order.save()
        send_mail(
            'Заказ не востребован',
            f'Здравствуйте, {order.user.username}. Ваш заказ #{order.id} был переведён в статус "Невостребован".',
            'your_email@gmail.com',
            [order.user.email],
        )
