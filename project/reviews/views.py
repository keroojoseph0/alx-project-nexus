from django.shortcuts import render
from .models import Review
from rest_framework.viewsets import ModelViewSet
from .serializers import ReviewSerializer

# Create your views here.

class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
