from django.db import models

class Role(models.TextChoices):
    ADMIN = "admin", "Admin"
    SELLER = "seller", "Seller"
    BUYER = "buyer", "Buyer"