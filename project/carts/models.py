from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product

# Create your models here.

User = get_user_model()



class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())


    def __str__(self):
        return self.user.email






class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)


    @property
    def total_price(self):
        return self.product.price * self.quantity
    
    def __str__(self):
        return self.cart.user.email