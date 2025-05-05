from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from .models import Order

@shared_task
def notify_ready_orders():
    orders = Order.objects.filter(status='ready_for_pickup')
    for order in orders:
        send_mail(
            'Ваш заказ готов к выдаче',
            f'Здравствуйте, {order.user.username}! Ваш заказ #{order.id} готов к выдаче.',
            'your_email@gmail.com',
            [order.user.email],
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
