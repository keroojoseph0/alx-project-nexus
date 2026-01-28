import random
from django.contrib.auth import get_user_model
from .models import EmailVerification
from .tasks import send_email

def send_verification_code(user_id):
    code = str(random.randint(100000, 999999))
    User = get_user_model()
    user = User.objects.get(id=user_id)


    EmailVerification.objects.create(
        user=user,
        code=code
    )

    subject = "Verification Code"
    message = f"Your verification code is: {code}"

    return send_email.delay(user_id, subject, message)