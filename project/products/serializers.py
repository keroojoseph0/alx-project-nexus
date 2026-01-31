from dataclasses import field
from rest_framework import serializers
from .models import Product, Category
from accounts.models import Role
from products.models import Category

class ProductSerializer(serializers.ModelSerializer):
    seller = serializers.PrimaryKeyRelatedField(read_only = True)

    class Meta:
        model = Product
        fields = ['id', 'name','seller', 'category','description', 'price', 'stock', 'created_at']
        read_only_fields = ['id', 'seller', 'created_at']

    
    def create(self, validated_data):
        validated_data['seller'] = self.context['request'].user
        return Product.objects.create(**validated_data)
    

    def validate(self, attrs):
        user = self.context['request'].user
        name = attrs.get('name')

        # CREATE
        if self.instance is None:
            if user.role != Role.SELLER:
                raise serializers.ValidationError("Only sellers can create products")

        # UPDATE
        else:
            if self.instance.seller != user:
                raise serializers.ValidationError("You can only update your own products")

        if Product.objects.filter(seller=user, name=name).exists():
            raise serializers.ValidationError(
                {'name': 'You already have a product with this name.'}
            )

        return attrs


class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = "__all__"

