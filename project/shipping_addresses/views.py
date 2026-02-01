from django.shortcuts import render
from rest_framework import viewsets
from .models import ShippingAddress
from .serializers import ShippingAddressSerializer

# Create your views here.


class ShippingAddressViewSet(viewsets.ModelViewSet):
    serializer_class = ShippingAddressSerializer

    def get_queryset(self):
        queryset = ShippingAddress.objects.filter(user=self.request.user)
        return queryset
