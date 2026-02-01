from django.contrib import admin
from .models import CartItem, Cart

# Register your models here.

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart__user', 'quantity', 'total_price']



@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user__email', 'total_price', 'is_ordered']

