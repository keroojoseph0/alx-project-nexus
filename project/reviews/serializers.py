from itertools import product
from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'user', 'product', 'rating', 'comment', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'user']

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user

        return super().create(validated_data)

    def validate(self, attrs):
        user = attrs.get('user')
        product = attrs.get('product')
        instance = self.instance

        if Review.objects.filter(user=user, product=product).exists():
            raise serializers.ValidationError("You have already reviewed this product.")

        if instance and instance.user != user:
                raise serializers.ValidationError("You cannot change this review.")

        return super().validate(attrs)