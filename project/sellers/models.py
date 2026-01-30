from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

class Status(models.TextChoices):
    PENDING = 'pending', 'Pending'
    APPROVED = 'approved', 'Approved'
    REJECTED = 'rejected', 'Rejected'


class SellerApplication(models.Model):
    seller = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller_application')
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)

    def __str__(self):
        return self.user.email
