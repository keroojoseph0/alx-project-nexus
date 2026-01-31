from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user__email', 'id', 'status', 'created_at', 'total_price']
    search_fields = ['user__eamil', 'status']
    ordering = ['created_at']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order__user__email', 'product__name', 'quantity', 'price']
