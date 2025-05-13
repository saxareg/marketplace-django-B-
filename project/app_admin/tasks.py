from django.core.mail import send_mail
from celery import shared_task


@shared_task
def send_approve_email(username, shop_name, email):
    send_mail(
        subject='Заявка на создание магазина отклонена',
        message=(
            f'Здравствуйте, {username}!\n\n'
            f'К сожалению, ваша заявка на создание магазина "{shop_name}" была отклонена.\n'
            f'Вы можете связаться с администрацией для уточнения причин.\n\n'
            'С уважением,\nАдминистрация Marketplace'
        ),
        recipient_list=[email],
        fail_silently=False,
    )


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
        recipient_list=[email],
        fail_silently=False,
    )
