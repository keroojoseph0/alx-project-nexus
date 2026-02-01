from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ShippingAddressViewSet


app_name = 'shipping_addresses'
router = DefaultRouter()

router.register(r'shipping-addresses', ShippingAddressViewSet, basename='shippingaddress')

urlpatterns = router.urls
