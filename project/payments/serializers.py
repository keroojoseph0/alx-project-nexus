from rest_framework import serializers
from orders.models import Order, OrderItem
from shipping_addresses.models import ShippingAddress
from carts.models import Cart


class CheckoutSerializer(serializers.Serializer):
    shipping_id = serializers.IntegerField(required = False)
    address_line1 = serializers.CharField(max_length = 255, required = False)
    address_line2 = serializers.CharField(max_length = 255, required = False, allow_blank = True)
    city = serializers.CharField(max_length = 100, required = False)
    state = serializers.CharField(max_length = 100, required = False)
    country = serializers.CharField(max_length = 50, required = False, default = 'Egypt')
    zipcode = serializers.CharField(max_length = 20, required = False)

    def validate(self, attrs):
        user = self.context['request'].user 

        try:
            cart = Cart.objects.get(user = user, is_orderd = False)
        except Cart.DoesNotExist:
            raise serializers.ValidationError("You don't have cart")
        if not cart.items.exists():
            raise serializers.ValidationError('your cart is empty')
        
        if not attrs.get('shipped_id'):
            required_fields = ['address_line1', 'city', 'state', 'country', 'zipcode']

            for field in required_fields:
                if not attrs.get(field):
                    raise serializers.ValidationError(f"{field} is required for new shipping address")
        else:

            try:
                shipping = ShippingAddress.objects.get(id = attrs.get('shipping_id'), user = user)
            except ShippingAddress.DoesNotExist:
                raise serializers.ValidationError('Invalid shipping address')
            
        return attrs
    
    def create(self, validated_data):
        user = self.context['request'].user 
        cart = Cart.objects.get(user = user, is_orderd = False)

        order = Order.objects.create()

        for item in cart.items.all():
            order.items.add(item)

        if validated_data.get('shipping_id'):
            shipping = ShippingAddress.objects.get(id = validated_data.get('shipping_id'), user = user)
            shipping.order = order
            shipping.save()
        else:

            shipping = ShippingAddress.objects.create(
                user = user,
                order = order,
                address_line1 = validated_data['addres_line1'],
                address_line2 = validated_data.get('addres_line2', ''),
                city = validated_data['city'],
                state = validated_data['state'],
                country = validated_data['country'],
                zipcode = validated_data['zipcode']
            )

        from .models import Payment, Status
        Payment.objects.create(order = order, amount = order.total_price, status = Status.PENDING)

        cart.is_ordered = True
        cart.save()

        return order

        
