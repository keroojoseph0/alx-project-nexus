from django.urls import path
from . import views 

app_name = 'payments'


urlpatterns = [
    path('checkout/', views.CheckoutViews.as_view(), name='checkout'),
]