from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['id', 'name']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'id', 'seller', 'category', 'stock', 'price']
    search_fields = ['category', 'id', 'name']
    ordering = ['name']