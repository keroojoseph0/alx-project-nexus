from os import read
from rest_framework import serializers
from .models import SellerApplication


class SellerApplicationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = SellerApplication
        fields = ['seller', 'status']
        read_only_fields = ['status']

    def create(self, validated_data):
        validated_data['seller'] = self.context['request'].user
        return super().create(validated_data)