from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CheckoutSerializer
from rest_framework import status

# Create your views here.


class CheckoutViews(APIView):
    def post(self, request):
        serializer = CheckoutSerializer(data = request.data, context = {'request': request})

        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        payment = order.payment 

        return Response({
            'order_id': order.id,
            'total': order.total_price,
            'status': order.status,
            'payment_id': payment.id,
            'payment_status': payment.status
        }, status= status.HTTP_201_CREATED)