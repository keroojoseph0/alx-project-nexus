from rest_framework import serializers
from .models import Order, OrderItem
from django.db import transaction

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'product_name', 'quantity', 'price', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'price', 'product_name', 'order']

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1.")
        return value



class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    user = serializers.ReadOnlyField(source = 'user.email')
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'total_price', 'status', 'created_at', 'updated_at', 'items']
        read_only_fields = ['id', 'status', 'created_at', 'updated_at', 'user', 'total_price']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user

        with transaction.atomic():
            order = Order.objects.create(user=user, **validated_data)
            total_price = 0

            for item_data in items_data:
                product = item_data['product']
                price = product.price * item_data['quantity']
                total_price += price

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item_data['quantity'],
                    price=price
                )

                
        order.total_price = total_price
        order.save()
        return order
    
    def validate_items(self, items):
        product_ids = [item['product'].id for item in items]

        if len(product_ids) != len(set(product_ids)):
            raise serializers.ValidationError(
                "Duplicate products are not allowed in the same order."
            )

        return items
    

    