from django.shortcuts import render
from sellers.models import SellerApplication
from .serializers import SellerApplicationSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

# Create your views here.


@api_view(['POST'])
def apply_as_seller(request):
    serializer = SellerApplicationSerializer(data=request.data, context = {'request': request})
    application = SellerApplication.objects.filter(seller=request.user).first()

    if serializer.is_valid():
        if not application:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if application.status == 'pending':
            return Response(
                {"detail": "Your application is under review."},
                status=status.HTTP_400_BAD_REQUEST
            )

        time_allowed_to_apply_again = (
            timezone.now() - application.created_at >= timezone.timedelta(days=30)
        )

        if time_allowed_to_apply_again:
            application.status = 'pending'
            application.created_at = timezone.now()
            application.save()

            return Response(
                SellerApplicationSerializer(application).data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            {"detail": "You can only reapply after 30 days from your last application."},
            status=status.HTTP_400_BAD_REQUEST
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
