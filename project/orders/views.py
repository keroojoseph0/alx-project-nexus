from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Order, Status
from .serializers import OrderSerializer
from rest_framework.response import Response
from rest_framework import status



# Create your views here.

class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(user=user).exclude(status=Status.CANCELED)
    
    def destroy(self, request, *args, **kwargs):
        order = self.get_object()

        order.status = Status.CANCELED
        order.save()

        return Response({"message": "Deleted successe"}, status=status.HTTP_200_OK)