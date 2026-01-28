from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import get_user_model

@shared_task
def send_email(user_id, subject, message):
    User = get_user_model()
    user = User.objects.get(id=user_id)

    send_mail(
        subject = subject,
        message = message,
        from_email = settings.DEFAULT_FROM_EMAIL,
        recipient_list = [user.email],
    )
