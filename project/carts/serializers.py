from genericpath import exists
from rest_framework import serializers
from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source = 'product.name')
    product_price = serializers.ReadOnlyField(source='product.price')

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product','product_name', 'quantity', 'product_price', 'total_price', 'created_at', 'updated_at']
        read_only_fields = ['id', 'cart', 'created_at', 'updated_at', 'product_price', 'total_price']



    def create(self, validated_data):
        cart = validated_data['cart']
        product = validated_data['product']
        quantity = validated_data.get('quantity', 1)



        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )

        if not created:
            item.quantity += quantity
            item.save()

        return item

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many = True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_price', 'created_at', 'updated_at', 'is_ordered']
        read_only_fields = ['id', 'user', 'created', 'updated_at', 'items', 'total_price']