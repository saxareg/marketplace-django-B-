from django.conf import settings
from django.core.mail import send_mail
from celery import shared_task


# Task to send an approval email when a shop creation request is accepted
@shared_task
def send_approve_email(username, shop_name, email):
    send_mail(
        subject='Заявка на создание магазина одобрена',  # Subject of the email
        message=(
            f'Здравствуйте, {username}!\n\n'
            f'Ваша заявка на создание магазина "{shop_name}" была успешно одобрена.\n'
            f'Теперь вы можете управлять своим магазином на платформе.\n\n'
            'С уважением,\nАдминистрация Marketplace'
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,  # Sender email from Django settings
        recipient_list=[email],  # Recipient's email address
        fail_silently=False,  # Raise error if sending fails
    )


# Task to send a rejection email when a shop creation request is denied
@shared_task
def send_reject_email(username, shop_name, email):
    send_mail(
        subject='Заявка на создание магазина отклонена',
        message=(
            f'Здравствуйте, {username}!\n\n'
            f'К сожалению, ваша заявка на создание магазина "{shop_name}" была отклонена.\n'
            f'Вы можете связаться с администрацией для уточнения причин.\n\n'
            'С уважением,\nАдминистрация Marketplace'
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )
